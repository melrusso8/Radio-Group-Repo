import ugradio
import astropy.coordinates
import astropy.time
import time
import numpy as np

interf = ugradio.interf.Interferometer()
obs = astropy.coordinates.EarthLocation(ugradio.nch.lon, ugradio.nch.lat, height=ugradio.nch.alt)
hpm = ugradio.hp_multi.HP_Multimeter()

#start data recording
hpm.start_recording(1)

for i in range(0, 120):
    #point telescopes
    print('Pointing!!!!!!!')
    t = astropy.time.Time(time.time(), format='unix')
    sun = astropy.coordinates.get_sun(t)
    altaz = astropy.coordinates.AltAz(obstime=t, location=obs)
    pointing = sun.transform_to(altaz)
    interf.point(pointing.alt.deg, pointing.az.deg)
    print('Pointed to : ' + str(interf.get_pointing()))
    print('Sun Coordinates : ra = ' + str(sun.ra.deg) + ', dec = ' + str(sun.dec.deg))

    #save data
    volts, times = hpm.get_recording_data()
    np.savez('lab3_sun_data.npz', volts=volts, times=times)

    #wait 30 seconds
    time.sleep(30)

#end data recording and stow telescope
interf.stow()
hpm.end_recording()