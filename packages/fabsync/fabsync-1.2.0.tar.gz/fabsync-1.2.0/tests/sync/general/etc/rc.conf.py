import re


def render(src, vars, get_content, **kwargs) -> bytes:
    return re.sub(rb'^pf_enable=.*$', b'pf_enable="YES"', get_content(), flags=re.M)
