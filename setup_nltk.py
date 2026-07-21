import nltk

packages = ['punkt', 'punkt_tab', 'stopwords']
success = True

for pkg in packages:
    if not nltk.download(pkg):
        print(f"Failed to download {pkg}")
        success = False

if success:
    print("NLTK components installed successfully.")
