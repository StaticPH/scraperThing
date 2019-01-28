from ngdata import start, fin

certFile = "D:\\msys2_64\\usr\\ssl\\certs\\ca-bundle.trust.crt"
oF = './test/t_dmp.json'

# rm ~/test/t_dmp.json 2>/dev/null;
def run(url):
	if type(url) != list:
		start(oF, [0, [url]], certFile)
	else:
		start(oF, [0, url], certFile)

#######################
# should be perfectly fine
#######################
run('https://giphy.com/gifs/help-computers-firstproblems-MhTVWcSgCKIbS')

#######################
# should be fixed
#######################
run('https://media.giphy.com/media/MhTVWcSgCKIbS/giphy.gif')

run('https://media.giphy.com/media/MhTVWcSgCKIbS/giphy.gifsadsad')

run('https://media.giphy.com/media/MhTVWcSgCKIbS/giphy.agifsadsad')

run('https://media.giphy.com/media/MhTVWcSgCKIbS/giphy.gifD')

run('https://media.giphy.com/media/MhTVWcSgCKIbS/giphy.gifDsdasdasd')

######################
# Group to be fixed
######################
run(['https://media.giphy.com/media/MhTVWcSgCKIbS/giphy.gif',
	 'https://media.giphy.com/media/MhTVWcSgCKIbS/giphy.gifsadsad',
	 'https://media.giphy.com/media/MhTVWcSgCKIbS/giphy.agifsadsad',
	 'https://media.giphy.com/media/MhTVWcSgCKIbS/giphy.gifD',
	 'https://media.giphy.com/media/MhTVWcSgCKIbS/giphy.gifDsdasdasd']
	)

#######################
# should be invalid match for handler
#######################
run('https://media.giphy.com//MhTVWcSgCKIbS/giphy.gifsadsad')

#######################
# nothing to scrape, causes failures when attempting to read url
#######################
# run('   ')
# run('""')
# run("'   '")
# run("' '")
# run("''")
# run("'''  '''")

#######################
# should be unknown handler
#######################
run("'''    a'''")
run("'''    ab'''")
run("'\'")
run("'a'")
run('0')
run('abababa')

#TODO: More exhaustive testing
#TODO: Consider using something like pytest or tox instead of this

#######################
# LAST STEP: close anything you opened
#######################
fin()