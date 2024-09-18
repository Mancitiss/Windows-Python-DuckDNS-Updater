def get_ipv6(string):
    for line in string.split("\n"):
        if "Temporary IPv6 Address" in line:
            # line looks like this
            # temporary ipv6 address. . . . . : 1234:5678:90ab:cdef:1234:5678:90ab:cdef
            # find the position of the first colon
            colon_index = line.find(":")
            # slice the string from the colon to the end
            ipv6 = line[colon_index+1:]
            ipv6 = ipv6.strip()
            return ipv6
    return None

def run(url, domains, token, ipv6 = None):
    # return if either url, domains, or token is None
    if url is None:
        raise ValueError("url is None, make sure DUCKDNS_URL environment variable is set")
    if domains is None:
        raise ValueError("domains is None, make sure DUCKDNS_DOMAINS environment variable is set")
    if token is None:
        raise ValueError("token is None, make sure DUCKDNS_TOKEN environment variable is set")

    # do it for ipv4 first
    import urllib.request
    import urllib.parse

    url_parts = urllib.parse.urlparse(url)

    params = {"domains": domains, "token": token}
    query = dict(urllib.parse.parse_qsl(url_parts.query))
    query.update(params)

    new_url = url_parts._replace(query=urllib.parse.urlencode(query)).geturl()
    print(new_url)

    with urllib.request.urlopen(new_url) as response:
        html = response.read()
        print(html)

    # now do it for ipv6
    if ipv6 is None:
        import subprocess
        output = subprocess.run("ipconfig".split(" "), capture_output=True, text=True)
        ipv6 = get_ipv6(output.stdout)

    print(ipv6)

    if ipv6 is not None:
        params["ipv6"] = ipv6

        url_parts = urllib.parse.urlparse(url)
        query = dict(urllib.parse.parse_qsl(url_parts.query))
        query.update(params)

        new_url = url_parts._replace(query=urllib.parse.urlencode(query)).geturl()
        print(new_url)

        with urllib.request.urlopen(new_url) as response:
            html = response.read()
            print(html)

def get_from_environment():
    import os
    url = os.environ.get("DUCKDNS_URL", "https://www.duckdns.org/update")
    domains = os.environ.get("DUCKDNS_DOMAINS", None) # if your domain is "abc.duckdns.org", set this to "abc"
    token = os.environ.get("DUCKDNS_TOKEN", None) # token from duckdns.org
    return url, domains, token

if __name__ == "__main__":
    url, domains, token = get_from_environment()
    run(url, domains, token)