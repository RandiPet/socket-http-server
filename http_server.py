import socket
import sys
import traceback
import os
import mimetypes


def response_ok(body=b"This is a minimal response", mimetype=b"text/plain"):
    """
    returns a basic HTTP response
    Ex:
        response_ok(
            b"<html><h1>Welcome:</h1></html>",
            b"text/html"
        ) ->

        b'''
        HTTP/1.1 200 OK\r\n
        Content-Type: text/html\r\n
        \r\n
        <html><h1>Welcome:</h1></html>\r\n
        '''
    """

    # DONE: Implement response_ok

    return b"HTTP/1.1 200 OK\r\nContent-Type: " + mimetype + b"\r\n\r\n" + body


def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""

    # DONE: Implement response_method_not_allowed
    return b"HTTP/1.1 405 Method Not Allowed"


def response_not_found():
    """Returns a 404 Not Found response"""

    # DONE: Implement response_not_found
    return b"HTTP/1.1 404 Not Found"


def parse_request(request):
    """
    Given the content of an HTTP request, returns the path of that request.

    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    """

    # DONE: implement parse_request
    if request.startswith('GET'):
        split_request = request.split(" ")
        return split_request[1]

    else:
        raise NotImplementedError


def response_path(path):
    """
    This method should return appropriate content and a mime type.

    If the requested path is a directory, then the content should be a
    plain-text listing of the contents with mimetype `text/plain`.

    If the path is a file, it should return the contents of that file
    and its correct mimetype.

    If the path does not map to a real location, it should raise an
    exception that the server can catch to return a 404 response.

    Ex:
        response_path('/a_web_page.html') -> (b"<html><h1>North Carolina...",
                                            b"text/html")

        response_path('/images/sample_1.png')
                        -> (b"A12BCF...",  # contents of sample_1.png
                            b"image/png")

        response_path('/') -> (b"images/, a_web_page.html, make_type.py,...",
                             b"text/plain")

        response_path('/a_page_that_doesnt_exist.html') -> Raises a NameError

    """

    # DONE: Raise a NameError if the requested content is not present
    # under webroot.
    if path.startswith('/') or path.startswith('\\'):
        path = path[1:]

    current_dir = os.path.dirname(__file__)
    the_path = os.path.join(current_dir, 'webroot', path)

    if not os.path.exists(the_path):
        raise NameError

    # DONE: Fill in the appropriate content and mime_type give the path.
    # See the assignment guidelines for help on "mapping mime-types", though
    # you might need to create a special case for handling make_time.py
    #
    # If the path is "make_time.py", then you may OPTIONALLY return the
    # result of executing `make_time.py`. But you need only return the
    # CONTENTS of `make_time.py`.

    if os.path.isfile(the_path):
        with open(the_path, "rb") as f:
            content = f.read()
        mime_type = mimetypes.guess_type(the_path)

    elif os.path.isdir(the_path):
        contents = os.listdir(the_path)
        content = ", ".join(contents)
        mime_type = 'text/plain'
        content = content.encode('utf8')

    mime_type = mime_type[0].encode('utf8')

    return content, mime_type


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break

                print("Request received:\n{}\n\n".format(request))

                # DONE: Use parse_request to retrieve the path from the request.
                try:
                    my_path = parse_request(request)
                    my_content, my_mimetype = response_path(my_path)
                    response = response_ok(my_content, my_mimetype)

                except NotImplementedError:
                    response = response_method_not_allowed()

                except NameError:
                    response = response_not_found()
                    
                # DONE: Use response_path to retrieve the content and the mimetype,
                # based on the request path.

                # DONE; If parse_request raised a NotImplementedError, then let
                # response be a method_not_allowed response. If response_path raised
                # a NameError, then let response be a not_found response. Else,
                # use the content and mimetype from response_path to build a 
                # response_ok.
                # response = response_ok(

                conn.sendall(response)

            except:
                traceback.print_exc()
            finally:
                conn.close() 

    except KeyboardInterrupt:
        sock.close()
        return
    except:
        traceback.print_exc()


if __name__ == '__main__':
    server()
    sys.exit(0)


