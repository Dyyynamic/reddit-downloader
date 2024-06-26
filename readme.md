# Reddit Downloader

Download images and videos from your saved posts on reddit

## Usage

1. Install requirements using ```pip install requests praw```
2. Go to https://www.reddit.com/prefs/apps and create a new app
3. Input your client id, client secret, password, user agent and username in ```downloader.py```
4. Run the program using ```python3 downloader.py```

## Supported Image hosts

- Reddit
- Imgur
- Gfycat

## TODO

- [x] Add reddit album support
- [x] Add colors to terminal output
- [x] Add gfycat support
- [x] Refactor main loop into separate functions
- [ ] Add v.redd.it support
- [ ] Add cross-post support
- [ ] Implement arguments, including error supression
- [ ] Implement better error handling (e.g. removed imgur images)
- [ ] Error on removed imgur posts

## Known Problems

- Cross-posts cause a www.reddit.com error
- requests.get errors when site is down
