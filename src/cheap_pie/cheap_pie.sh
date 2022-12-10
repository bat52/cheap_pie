
#!/bin/bash
# create ipython default start with cheap_pie initialization
START=start.ipy 
rm $START

echo "%load_ext autoreload" > $START
echo "%autoreload" >> $START
echo "# %reset" >> $START
echo "%run ./cheap_pie_core/cheap_pie.py $@" >> $START
echo "%tb" >> $START 

# add start to ipython default
cp $START ~/.ipython/profile_default/startup/
# call ipython (will automatically launch cheap_pie)
ipython3
# remove cheap_pie start from ipython default
rm ~/.ipython/profile_default/startup/$START