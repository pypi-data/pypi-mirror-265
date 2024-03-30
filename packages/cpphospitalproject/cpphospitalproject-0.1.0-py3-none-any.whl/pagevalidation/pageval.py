def pass_validation(passwd, re_passwd):
    if passwd != re_passwd:
        return 'Passwords do not match.'
    if re_passwd is None:
        return 'Enter Re-Password.'
    if passwd is None:
        return 'Enter Password.'
    return ""