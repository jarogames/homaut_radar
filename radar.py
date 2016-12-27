#!/home/mraz/anaconda3/bin/python3
import os
#import Image
import time
import matplotlib
matplotlib.use('Agg')  #  DISPLAY=:0  not necessary BEFORE pyplot imported!!!
import matplotlib.pyplot as plt
####import matplotlib.image as mpimg
from scipy.misc import imread
import matplotlib.cbook as cbook

import numpy as np






def get_picture(dest='web'):
	rname='annotation_placeholder'
	if ( dest=='web'):
### GET last picture name
		a=os.popen('wget -q http://www.chmi.cz/files/portal/docs/meteo/rad/data_tr_png_1km/ -O - |  grep png | awk -F \\\"  \'{print $2 }\' | sort | tail -1')
		rname=a.readline() 
		tmppng='/tmp/'+rname.rstrip()
		print('i.... remote name=',tmppng)
		os.system('wget -c http://portal.chmi.cz/files/portal/docs/meteo/rad/data_tr_png_1km/'+ rname.rstrip() +' -O '+tmppng)
		return tmppng
	if ( dest=='debug'):
		tmppng='i.png'
		os.system('wget -c http://portal.chmi.cz/files/portal/docs/meteo/rad/data_tr_png_1km/pacz23.z_max3d.20160917.1500.0.png -O '+tmppng)
		print('i.... remote name=',tmppng)
###os.system('cp i.png  '+tmppng)  ### jakoby wget
		return tmppng
	if ( dest=='test1'):
		tmppng='/tmp/test1.png'
		print('i.... remote name=',tmppng)
		return tmppng


def make_circle( cil ):
	samplesize=cil[2]
	circle1=[ cil[0],cil[1], cil[0]+1, cil[1]+1  ]
	circle2=[ cil[0],cil[1], cil[0]+3, cil[1]+3  ]
	circle3=[ cil[0],cil[1], cil[0]+samplesize/2, cil[1]+samplesize/2  ]
	rect1=[ cil[0] -samplesize/2,cil[1]-samplesize/2, cil[0]+samplesize/2, cil[1]+samplesize/2  ]
	#fuch='circle '
	#print( fuch , ','.join( map(str,circle3) ) )
	#CMD1=' -fill fuchsia -draw \"circle '+','.join( map(str,circle3) ) +'\" '
	CMD1=' -fill fuchsia -draw \"rectangle '+str(rect1[0])+','+str(rect1[1])+' '+str(rect1[2])+','+str(rect1[3])+'\" '
	CMD2=' -fill white   -draw \"circle '+','.join( map(str,circle2) ) +'\" '
	CMD3=' -fill fuchsia -draw \"circle '+','.join( map(str,circle1) ) +'\" '
	#print('test1 ',CMD1+CMD2)
	CMD='convert '+tmppng+' '+CMD1+CMD2+CMD3+' '+tmpcirc
	print('CIRC...:',CMD)
	if (os.system( CMD )!=0):
		print('error with '+CMD)
		exit(1)
	#samplesize=120
	crop=str(samplesize)+'x'+str(samplesize)+'+'+str(cil[0]-round(samplesize/2))+'+'+str(cil[1]-round(samplesize/2))
	#print( 289- round(samplesize/2 ) )  #9x9+285+314
	CMD='convert '+tmppng+'  -crop '+crop+' '+tmpsample
	print('CROP99...',CMD)
	if (os.system( CMD )!=0):
		print('error with '+CMD)  
		exit(1)
	rgb=[
	 [56,0,112],
	 [48,0,168],
	 [0,0,252],
	 [0,108,192],
	 [0,160,0],
	 [0,188,0],
	 [52,216,0],
	 [156,220,0],
	 [224,220,0],
	 [252,176,0],
	 [252,132,0],
	 [252,88,0],
	 [252,0,0],
	 [160,0,0],
	 [252,252,252]
	 ]
	factor=[0.056, 0.1, 0.178, 0.315, 0.56, 1.0, 1.78, 3.15, 5.6, 10., 17.8, 31.5, 56., 100., 178. ]
	intensity=[]
	for i in range( len(rgb)):
		RGB='\"rgb('+','.join( map(str,rgb[i]))+')\"'
		CMD='convert '+tmpsample+' -fill black +opaque '+RGB+' -fill white -opaque '+RGB+' -format "%[fx:mean*'+str(factor[i])+']\\n" info: '
	#	CMD='convert '+tmpsample+' -fill black +opaque '+RGB+' -fill white -opaque '+RGB+' -format "%[fx:mean*'+str(1.0)+']\\n" info: '
		#print('ANA1...',CMD)
		a=os.popen(CMD)
		inten=a.readline().rstrip()
		intensity.append( float(inten) )
		print(i,inten)  
	print('SUM=',sum(intensity))
	return intensity,factor
####################################################################






#####################################################################
#####################################################################
#
#
#          MAIN 
#
#####################################################################
#####################################################################



#tmppng='/tmp/radar.png'
#tmppng='i.png'
#tmppng=get_picture('test1')  #####################
tmppng=get_picture('web')  #####################
print('ahoj')
tmpcirc='/tmp/i2.png'
tmpcrop='/tmp/i3.png'
tmpcropa='/tmp/i3a.png'  # annotated
tmpsample='/tmp/i4.png'
###### DATE.  bash.
CURRENTTIME='date +%Y%m%d_%H%M%S'
a=os.popen( CURRENTTIME )
currenttime=a.readline().rstrip()
### CREATE             things to store in /motion
os.system(' mkdir -p  /motion/cam_radar/')
os.system(' mkdir -p  /motion/cam_radarana/')
motionradar='/motion/cam_radar/'+currenttime+'.jpg'
motionradarana='/motion/cam_radarana/'+currenttime+'.jpg'
#### camradar.gif  in  myweb
gifradar='/tmp/camradar.gif'

time.sleep(1)
##################### I HAVE ALL FILES #####################

samplesize=9
#mnisek=[289,318, samplesize  ]  #  coord.,  samplesize=9
mnisek=[288,313, samplesize  ]  #  coord.,  samplesize=9
revnice=[282,307,samplesize  ]  #  coord.,  samplesize=9
praha=[301,292,  samplesize  ]  #  coord.,  samplesize=9
snezka=[3394,221,  samplesize  ]  #  coord.,  samplesize=9
rez= [296,280, samplesize ]
rana= [252,261, samplesize ]
bratri= [294,349, samplesize ]

cr=[301,305,  180  ] 

icr,factor = make_circle( cr )
icrev,factor = make_circle( revnice )

intensity,factor = make_circle( mnisek )  # LAST WILL HAVE PICTURE
#intensity,factor = make_circle( revnice )

##################################### 9x9  SAMPLE OK
#################################################  CIRCLE IS OK now


time.sleep(1)
######################### i have intensity,factor
x=np.arange( len(factor) )
npi=np.array( intensity )
npicr=np.array( icr )
npirev=np.array( icrev )
npf=np.array( factor )



CMD='convert  '+tmpcirc+' -crop 266x200+150+205 -resize 360x300 -background white -alpha remove '+tmpcrop
print('CROP...:',CMD)
if (os.system( CMD )!=0):
	print('error with '+CMD)
	time.sleep(1)

	exit(1)
time.sleep(1)

######################################### CROP OK


#CMD='convert '+tmpcrop+' -fill white -gravity center -font Arial -pointsize 24  -undercolor \'#00000080\'  -annotate -150+120 %t '+tmpcropa
CMD='convert '+tmpcrop+' -fill white -gravity center -font Arial -pointsize 14  -undercolor \'#00000080\'  -annotate -150+120 "'+tmppng+'" '+tmpcropa
print('FNAME...',CMD)
if (os.system( CMD )!=0):
	print('error with '+CMD)
	time.sleep(1)

	exit(1)
time.sleep(1)

######################################## CROP WITH FILENAME OK



CMD='convert  '+tmpcropa+' '+ motionradar
print('RM...',CMD)
if (os.system( CMD )!=0):
	print('! error with '+CMD)  
	time.sleep(3)
	exit(1)

########################################  convert to jpg, nightly motion needs jpg


print('before fig')
time.sleep(5)


fig = plt.figure( figsize=(6, 5), dpi=100 )
#fig = plt.figure(  )
print('after fig')
time.sleep(5)

ax = fig.add_subplot(111)

#plt.bar(  x, npi )
#plt.bar(  x, npi/npf )
width = 0.2                      # the width of the bars

#### RULE:
##### the last p[icture MNISEK
##### the first BAR  CR
## the bars
#CR
print('before bar')
time.sleep(2)

rects1cr = ax.bar( x , npicr, 1.0,
                color='dimgray'   )
#NUMBERS NORMALIZED
rects2 = ax.bar(x, npi/npf, width,
                    color='white'  )

#mnisek
rects1 = ax.bar( x+1*width , npi, width,
                color='blue'   )
#revnice
rects1rev = ax.bar( x+2*width , npirev, width,
                color='cyan'   )



#chartreuse   http://matplotlib.org/examples/color/named_colors.html
#orange
#dimgray
print('before matplotlib')
time.sleep(2)

matplotlib.rcParams['examples.directory']='.' 
datafile = cbook.get_sample_data( tmpsample , asfileobj=True )
img = imread(datafile)
######## fig.set_size_inches(18.5, 10.5)
matplotlib.rcParams['figure.figsize'] = 5, 10

#plt.imshow(img, zorder=0, extent=[0,16,0, max(npi) ]  )

plt.imshow(img, zorder=0, extent=[1,16,0, max(  max(npicr),max(npirev),max(npi),max(npi/npf) ) ]  , aspect='auto', interpolation='none')



# axes and labels
#plt.plot( npf, npi, 'ro')

		#img = mpimg.imread( tmpsample )
		#plt.imshow(img)   # i add implot=
#plt.show()
plt.savefig( motionradarana )
time.sleep(2)



RMCMD='rm '+tmppng+'; rm '+tmpcirc+';  rm '+tmpcrop+'; rm  '+tmpcropa+'; rm '+tmpsample
#if (os.system( RMCMD )!=0):
	#print('error with '+RMCMD)  
#	exit(1)

###########
#
##  create GIF
#
gifie=[]
CMD='cd /motion/cam_radar; ls -1tr 20*.jpg | tail -4 '
a=os.popen(CMD) 
time.sleep(2)

while 1:
	gifie1=( a.readline().rstrip() )
	print( '   ... files : gifie1 ')
	if not gifie1:
		break
	gifie.append( gifie1 )
time.sleep(1)

CMD='cd /motion/cam_radar;convert -resize 360x300 -delay 60 '+' '.join(gifie)+'  -loop 0  '+gifradar
print('GIF prepare:' ,CMD)
if ( os.system(CMD)!=0):
	print('... problem with ',CMD)
	time.sleep(1)
	exit(1)

######################
#
#   SQMYLITE 
##
#  rain3   mnisek  CR   revnice
#  rain5   mnisek  CR   revnice  bratri  rez  
CMD='sqmylite -i rain3.mysql '+str(sum(npi))+' '+str(sum(npicr))+' '+str(sum(npirev))
print( 'saving to sqmylite ... '+CMD )
if (os.system(CMD) !=0):
	print('error with '+CMD)  
	time.sleep(1)

	exit(1)
#os.system('sqmylite -i rain3.mysql  ', sum(npi),sum(npicr),sum(npirev)  )

print(' echo sleeping 900 sec for the next frame ....')
time.sleep(900)
