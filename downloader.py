import re
import requests
import sys
import os

def transform_url(response):
    # Extract the HTML content from the response
    html_content = response.text

    # Search for the specific string beginning with "https://player-vz" and extract it
    match = re.search(r'https://player-vz[^"]+', html_content)
    if match:
        matched_string = match.group(0)

        # Extract the value after "?v=" using regex
        video_id_match = re.search(r'\?v=([\w-]+)', matched_string)
        if video_id_match:
            video_id = video_id_match.group(1)

            # Remove the unnecessary part from the matched string
            trimmed_string = matched_string.replace("/embed/?v=" + video_id, "")

            # Perform the required string transformation
            transformed_url = trimmed_string.replace("player-vz", "b-vz") + '/' + video_id + '/video.m3u8'
            player_url = trimmed_string.replace("embed/?v=" + video_id, "")
            return transformed_url, player_url

    # Return None if the specific string is not found
    return None, None

def execute_binary(binary_path, transformed_url, player_url):
    # Build the command
    command = f"{binary_path} {transformed_url} -H 'referer: {player_url}' -sv best"

    # Execute the command
    os.system(command)

if len(sys.argv) < 2:
    print("Usage: python script.py <url> [-H header_name:header_value]... [--headers-file <file_path>] [-C cookies]")
    sys.exit(1)

url = sys.argv[1]
headers = {}
cookies = {}  # Initialize the cookies dictionary

# Parse the command-line arguments for additional headers and cookies
i = 2
headers_file_path = None

while i < len(sys.argv):
    if sys.argv[i] == '--headers-file' and i + 1 < len(sys.argv):
        headers_file_path = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == '-H' and i + 1 < len(sys.argv):
        if headers_file_path is not None:
            print("Error: Cannot use both -H and --headers-file parameters simultaneously.")
            sys.exit(1)
        header_parts = sys.argv[i + 1].split(':')
        if len(header_parts) == 2:
            header_name = header_parts[0].strip("'").strip()
            header_value = header_parts[1].strip("'").strip()
            headers[header_name] = header_value
        i += 2
    elif sys.argv[i] == '-C' and i + 1 < len(sys.argv):
        cookies_input = sys.argv[i + 1]
        cookies_list = cookies_input.split("; ")
        for cookie in cookies_list:
            name, value = cookie.split("=")
            cookies[name] = value
        i += 2
    else:
        print("Error: Invalid arguments")
        sys.exit(1)

# If headers file is provided, read the file and add the headers
if headers_file_path is not None:
    try:
        with open(headers_file_path, 'r') as headers_file:
            for line in headers_file:
                line = line.strip()
                if line:
                    header_parts = line.split(':')
                    if len(header_parts) == 2:
                        header_name = header_parts[0].strip("'").strip()
                        header_value = header_parts[1].strip("'").strip()
                        headers[header_name] = header_value
    except IOError:
        print("Error: Failed to read the headers file:", headers_file_path)
        sys.exit(1)

# If cookies are provided, add them to the headers
if cookies:
    headers["Cookie"] = "; ".join([f"{name}={value}" for name, value in cookies.items()])

# Send a GET request with the provided headers and cookies (if any)
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    transformed_url, player_url = transform_url(response)
    if transformed_url:
        print("Transformed URL:", transformed_url)
        print("Player URL:", player_url)
        execute_binary("N_m3u8DL-RE_Beta_linux-x64/N_m3u8DL-RE", transformed_url, player_url)
    else:
        print("Failed to find the specific string in the HTML content.")
else:
    print("Request failed with status code:", response.status_code)
