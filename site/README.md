# How to use

Here's how to add content to the site, and then deploy it.

## Adding Content

1. Open the content folder
2. If you are adding to a subfolder (like meeting minutes, or topics), make a copy the `template.md` in that folder and give it a new name. Otherwise just edit the markdown document inside of `content/` as needed.
3. Edit the template/markdown file as it asks you to
4. Commit your work to master.
5. Done.

## Deploying updates to site

Once you have content written and committed, you need to deploy your changes with `Hugo`. This means you'll either run `./publish.sh` to have it do it for you, or just message to the group and someone else can quickly build it for you (who has everything setup).

If you'd like to run `publish.sh` you need to have the following figured out:
1. Install [hugo](https://gohugo.io/getting-started/installing/). I HIGHLY recommend just downloading the binary, and placing it in your PATH. Saves you some hassle. Or use brew if you are on Mac.
2. You need git higher than 2.5 installed. If you update your git, you should be fine.
3. Modify publish.sh to be executable if it's not already (`chmod +x publish.sh`)

Now you can run publish.sh. After running it, simply CD into the public folder and push the changes. Github will update shortly after.