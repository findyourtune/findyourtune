npm run build

cd dist

echo Deploying...

git init

git add -A

git commit -m 'Deploying to gh-pages'

git push -f git@github.com:findyourtune/findyourtune.git gh-pages