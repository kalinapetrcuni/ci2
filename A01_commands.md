# A01 commands to solve assignment

I used the following commands to fullfil the assignment:

```bash
ssh-keygen # to generate an rsa key pair

# Encountered failed authentications. 
# Realized the ssh agent did not add the private key as an identity

ssh-add ~/.ssh/ci2 # to add the newly created private key
ssh-add -l # list the current identities (hopefully including the new key)
ssh -T git@github.com # test connectivity to GitHub

git clone git@github.com:kalinapetrcuni/ci2.git # clone the repository

git add AO1_commands.md # add this file to be tracked by git
git add README.md # likewise with the readme

git commit -m "The commit message here"
git push # push the changes to GitHub
 
```




