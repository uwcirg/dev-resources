from prodanon.transformers.users import email_for_user


def test_id_in_email():
    b4 = 'user@gmail.com'
    after = email_for_user(112233, b4)
    assert after.split('+')[1].startswith("112233")
    assert 'user' not in after
    

def test_nested_prefix():
    b4 = '__deleted_1640755691____invite__achen2401+99000@gmail.com'
    after = email_for_user(1234, b4)
    assert after.startswith(b4[:32])
