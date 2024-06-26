import requests, time, praw, pathlib
from urllib.parse import urlparse

# Debug info
start_time = time.time()  # Start timer
file_counter = 0
error_urls = []


class colors:
	GREEN = '\033[92m'
	BLUE = '\033[94m'
	RED = '\033[91m'
	RESET = '\033[0m'

REDDIT = praw.Reddit(
	client_id='',
	client_secret='',
	password='',
	user_agent='',
	username=''
)

SAVED_POSTS = REDDIT.user.me().saved(limit=1000)


def download(url, host, subreddit, filename):
	print(f'[{colors.BLUE + host + colors.RESET}] Downloading {filename}...', end='')
	path = f'output/{subreddit}/{filename}'

	response = requests.get(url)
	with open(path, 'wb') as file:
		file.write(response.content)

	print(colors.GREEN + ' Done' + colors.RESET)
	return True  # Should return based on download success


def print_debug_results():
	end_time = time.time()
	total_time = end_time - start_time

	print(f'\nDownloaded {file_counter} files.')
	print(f'Program took {total_time:.2f} seconds to finish.')
	print(f'Encountered {len(error_urls)} error(s).')

	if len(error_urls) > 0:
		print('\nError URLs:')
		for url in error_urls:
			print(url)


def download_gfycat(post, subreddit, host, path):
	gfyid = path.split('/')[-1].split('-')[0].lower()
	filename = gfyid + '.mp4'

	# Get mp4 url through gfycat api
	api_url = f'https://api.gfycat.com/v1/gfycats/{gfyid}'
	gfycat = requests.get(api_url).json()

	url = gfycat['gfyItem']['content_urls']['mp4']['url']
	return download(url, host, subreddit, filename)


def download_imgur_reddit(url, subreddit, host, path):
	filename = path.split('/')[-1]  # e.g. file.gif
	extension = filename.split('.')[-1]  # e.g. gif

	# Handle imgur gifv videos
	if extension == 'gifv':
		url = url.replace('.gifv', '.mp4')
		filename = filename.replace('.gifv', '.mp4')

	# Download file
	return download(url, host, subreddit, filename)


def download_gallery(post, subreddit, host):
	success = []

	for item in post.media_metadata.items():
		url = item[1]['p'][0]['u']  # Get url from metadata
		url = url.split('?')[0].replace('preview', 'i')  # Reformat url
		filename = url.split('/')[-1]  # e.g. file.gif

		# Download file
		success.append(download(url, host, subreddit, filename))

	return all(success)


def main():
	global file_counter

	for post in SAVED_POSTS:
		# Check for missing gallery items or image url
		if hasattr(post, 'is_gallery'):
			if not hasattr(post.media_metadata, 'items'):
				continue  # Missing gallery items, continue
		elif not hasattr(post, 'url'):
			continue  # Missing image url, continue

		url = post.url
		subreddit = post.subreddit.display_name

		# Make directory for subreddit if not exists
		pathlib.Path('output/' + subreddit).mkdir(parents=True, exist_ok=True)

		# Parse url using urllib
		result = urlparse(url)
		host = result.hostname
		path = result.path

		success = False

		if host == 'gfycat.com':
			success = download_gfycat(post, subreddit, host, path)
		elif host in ('i.imgur.com', 'i.reddit.com', 'i.redd.it'):
			success = download_imgur_reddit(url, subreddit, host, path)
		elif hasattr(post, 'is_gallery'):
			success = download_gallery(post, subreddit, host)
		else:
			print(f'{colors.RED}Error{colors.RESET}: Host {host} is unsupported.')

		if success:
			post.unsave()
			file_counter += 1
		else:
			error_urls.append(url)

	print_debug_results()


if __name__ == '__main__':
	main()
