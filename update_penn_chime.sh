cd ./chime
git pull
cd ..
cd mychime
rm -r penn_chime/*
rmdir penn_chime
cp -r ../chime/src/* .
cp settings_bh.py penn_chime/settings.py
