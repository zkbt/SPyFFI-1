'''A few simple tests of the TESS image simulation tools.'''
import Camera
from imports import *


def foral(diffusion=False, testpattern=False):
	sub(n=90000, subarray=32, cadence=2, jitter=False, testpattern=True, remake=True, diffusion=False)

def sub(ra=270, dec=66.56070833333332, cadence=2, n=1, subarray=100, jitter=False, testpattern=True, remake=True, diffusion=False, display=False):
	C = Camera.Camera(subarray=subarray,testpattern=testpattern)
	C.setCadence(cadence)
	#C.point(ra, dec)
	I = C.ccds[0]
	I.display=False
	if jitter:
		I.label += 'jittered'
	else:
		I.label += 'unjittered'
	I.display = display
	for i in range(n):
		I.expose(write=True, split=False, jitter=jitter, remake = remake &(i == 0), smear=False, terse=False, diffusion=diffusion)
		print C.ra
	return C, I


def create(ra=270, dec=66.56070833333332, cadence=1800, n=5):
	C = Camera.Camera(ra=ra, dec=dec)
	C.setCadence(cadence)
	I = C.ccds[2]
	for i in range(n):
		I.expose(write=True)

def orion():
	create(82, 1)

def subtractPairs(ra=82, dec=1,cadence=2):
	C = Camera.Camera()
	C.setCadence(cadence)
	C.point(ra, dec)
	I = tess.Image(C)
	g = glob.glob(I.directory + 'final*')
	for i in range(len(g)-1):
		this = I.loadFromFITS(g[i])
		that = I.loadFromFITS(g[i+1])
		filename = I.directory + g[i+1].split('/')[-1].split('.')[0] + '-' + g[i].split('/')[-1].split('.')[0] + '.fits'
		I.writeToFITS(that - this, filename)


def threefields():
	# north celestial pole
	create(ra=270, dec=66.56070833333332, cadence=1800, n=1)
	# north galactic pole
	create(ra=192.25, dec=27.4, cadence=1800, n=1)
	# galatic center
	create(ra=266.4166666666667, dec=-29.00777777777778, cadence=1800, n=1)

def forPT():
	pointings = [(270,66.56070833333332), (192.25,27.4), (266.4166666666667,-29.00777777777778)]
	C = Camera.Camera()
	for pos in pointings:
		ra, dec = pos
		C.setCadence(1800)
		C.point(ra, dec)
		C.project(write=True)

def forEd():
