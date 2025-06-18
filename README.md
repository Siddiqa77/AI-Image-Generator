#add .env in .gitignore command
#echo .env >> .gitignore


# file remove from Github
git rm -r --cached .streamlit
git commit -m "Remove .streamlit folder from tracking"
git push
