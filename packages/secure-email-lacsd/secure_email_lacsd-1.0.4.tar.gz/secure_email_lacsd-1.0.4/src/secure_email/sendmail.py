from __future__ import annotations

import mimetypes
import platform
import smtplib
import ssl
import traceback
from email.message import EmailMessage
from logging.handlers import SMTPHandler
from pathlib import Path
from typing import Optional, Union

try:
    import keyring
except ImportError:
    pass

machine = platform.node().lower()


class Emailer:
    def __init__(
        self,
        secure_host: str,
        port: int,
        email_address: str,
        password: Optional[str] = None,
        user: Optional[str] = None,
        unsecure_host: str = "",
        use_keyring: bool = False,
        include_ssl_status: bool = False,
    ) -> None:
        self.secure_host: str = secure_host
        self.include_ssl_status: bool = include_ssl_status
        self.bu_host: str = unsecure_host
        self.port: int = port
        self.email_address: str = email_address
        self.user: str = user or email_address
        self.password: str = password or ""
        if use_keyring:
            self.password = keyring.get_password(self.email_address, self.user) or ""
            pass

    def __send(
        self,
        to: Union[str, list[str]],
        subject: str,
        body: str,
        attachments: list[str] = [],
        cc_list: list[str] = [],
        bcc_list: list[str] = [],
        html: bool = False,
        secure: bool = True,
    ) -> str:
        """
        Sends STMP email over TLS using SSL

        params
        ------
        to (str|list[str]): email recipient(s)
        subject (str): email subject line
        body (str): body of email as text or HTML string
        cc_list (list[str]): recipients to CC (default: [])
        bcc_list (list[str]): recipients to BCC (default: [])
        html (bool): whether to send body as HTML (default: False)
        secure (bool): whether to send with SSL (default: True)

        returns
        -------
        response (subprocess.CompletedProcess): exit code returned by cmd.exe after executing
            email send command
        """

        status_str: str = "SSL" if secure else "non-SSL backup host"
        newline: str = "\n"
        if self.include_ssl_status:
            if html:
                body += f"<p>Email sent over {status_str}</p>"
            else:
                body += f"{newline}{newline}*** Email sent over {status_str} ***"
        to = to if isinstance(to, str) else ",".join(to)

        smtp_server = self.secure_host if secure else self.bu_host
        msg = EmailMessage()
        if html:
            msg.set_content(body, subtype="html")
        else:
            msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = self.email_address
        msg["To"] = to
        if cc_list is not None:
            msg["CC"] = ",".join(cc_list)
        if bcc_list is not None:
            msg["BCC"] = ",".join(bcc_list)
        for attachment in attachments:
            filename = Path(attachment).name
            mimetype, _ = mimetypes.guess_type(attachment)
            if mimetype is None:
                continue
            maintype, subtype = mimetype.split("/")
            readmode = "r" if maintype == "text" else "rb"
            kwargs = {"filename": filename}
            if maintype != "text":
                kwargs["maintype"] = maintype
                kwargs["subtype"] = subtype
            with open(attachment, readmode) as f:
                content = f.read()
                msg.add_attachment(content, **kwargs)  # type: ignore
        if secure:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        try:
            with smtplib.SMTP(smtp_server, self.port) as server:
                if secure:
                    server.starttls(context=context)
                    server.login(self.email_address, self.password)
                server.send_message(msg)
                return "success"
        except Exception as e:
            return f"{e}: {traceback.format_exc}"

    def send(
        self,
        to,
        subject: str,
        body: str,
        attachments: list[str] = [],
        cc_list: list[str] = [],
        bcc_list: list[str] = [],
        html: bool = False,
    ) -> str:
        """
        Sends STMP email over TLS using SSL

        params
        ------
        to (str|list[str]): email recipient(s)
        subject (str): email subject line
        body (str): body of email as text or HTML string
        cc_list (list[str]): recipients to CC (default: [])
        bcc_list (list[str]): recipients to BCC (default: [])
        html (bool): whether to send body as HTML (default: False)

        returns
        -------
        response (subprocess.CompletedProcess): exit code returned by cmd.exe after executing
            email send command
        """
        args = [to, subject, body]
        kwargs = {
            "attachments": attachments,
            "cc_list": cc_list,
            "bcc_list": bcc_list,
            "html": html,
        }
        response = self.__send(*args, **kwargs)
        if response != "success":
            response = self.__send(*args, **kwargs, secure=False)
        return response


class EmailHandler(SMTPHandler):
    def __init__(
        self,
        mailhost,
        fromaddr: str,
        toaddrs,
        subject: str,
        credentials=None,
        secure=None,
        timeout: float = 5,
        send_html: bool = False,
        backup_host: str = "",
        include_ssl_status: bool = False,
    ) -> None:
        super().__init__(
            mailhost, fromaddr, toaddrs, subject, credentials, secure, timeout
        )
        self.send_html = send_html
        self.emailer = Emailer(
            (
                self.mailhost.split(":")[0]
                if isinstance(self.mailhost, str)
                else self.mailhost[0]
            ),
            self.mailport or 0,
            self.fromaddr,
            password=credentials[1] if credentials else None,
            use_keyring=False if credentials else True,
            unsecure_host=backup_host,
            include_ssl_status=include_ssl_status,
        )

    def emit(self, record) -> None:
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            result = self.emailer.send(
                self.toaddrs,
                self.getSubject(record),
                self.format(record),
                html=self.send_html,
            )
            if result != "success":
                print(result)
        except Exception:
            self.handleError(record)
