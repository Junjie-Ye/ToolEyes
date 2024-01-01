import zmail


def send(
    to_email: str,
    subject: str,
    content: str,
    cc: str = None,
    login_email: str = "",
    login_password: str = ""
):
    server = zmail.server(login_email, login_password)
    mail_data = {
        "subject": subject,
        "content_text": content
    }
    return server.send_mail(to_email, mail_data, cc=cc)


def send_list(
    to_email_list: list,
    subject: str,
    content: str,
    cc: str = None,
    login_email: str = "",
    login_password: str = ""
):
    server = zmail.server(login_email, login_password)
    mail_data = {
        "subject": subject,
        "content_text": content
    }
    return server.send_mail(recipients=to_email_list, mail=mail_data, cc=cc)


def recieve_latest(
    login_email: str = "",
    login_password: str = ""
):
    server = zmail.server(login_email, login_password)

    latest_mail = server.get_latest()
    zmail.show(latest_mail)


def recieve_id(
    id: int,
    login_email: str = "",
    login_password: str = ""
):
    server = zmail.server(login_email, login_password)

    recieve_mail = server.get_mail(id)
    zmail.show(recieve_mail)


def recieve_list(
    subject: str = None,
    sender: str = None,
    login_email: str = "",
    login_password: str = ""
):
    server = zmail.server(login_email, login_password)

    mails = server.get_mails(subject=subject, sender=sender)
    zmail.show(mails)


if __name__ == '__main__':
    # print(send(
    #   to_email="1479106701@qq.com",
    #   subject="Hello World",
    #   content="Hello World, this is Liusc."
    # ))
    # print(send_list(
    #   to_email_list=["1479106701@qq.com","liusc2020@gmail.com"],
    #   subject="Hello World",
    #   content="Hello World, this is Liusc."
    # ))
    # print(recieve_latest())
    # print(recieve_id(4))
    pass
