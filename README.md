# TimeDil
A simple command-line time dilation calculator. 

## Usage
```
usage: timedil.py [-h] [-s SPEED | -ms METERSPERSEC] [-l LIGHTYEARS]
                  [-sl SHIPLENGTH] [-p PRECISION] [-m MASS]

optional arguments:
  -h, --help            show this help message and exit
  -s SPEED, --speed SPEED
                        Speed expressed as a multiple of the speed of light.
                        Speed of light = 1
  -ms METERSPERSEC, --meterspersec METERSPERSEC
                        Speed expressed in meters per second
  -l LIGHTYEARS, --lightyears LIGHTYEARS
                        Light-years to travel
  -sl SHIPLENGTH, --shiplength SHIPLENGTH
                        Length of your ship in meters
  -p PRECISION, --precision PRECISION
                        Number of decimal places. Defaults to 6.
  -m MASS, --mass MASS  Mass of your ship in tons. Defaults to 10.
```

The `--speed` and `--meterspersec` are mutually exclusive options. 

The `--speed` option is for specifying speeds as a proportion of the speed of light from `0` to `1`. `0` would be no speed at all, `1` would be the speed of light exactly (299,792,458 m/s), and `0.5` is half the speed of light (149,896,229.0 m/s):
```
~/wunderhund/timedil(master*) » ./timedil.py -s 0.5 -l 4.3                              
Lightyears to travel:  4.3
Speed in m/s:  149,896,229.0 m/s
Percent of c:  50.0 %
Lorentz Factor:  1.1547005383927808619404231649241410195827484130859375
Observer Time:  8 years, 7 months, 6 days, 2 hours, 5 minutes, 54 seconds
Ship Time:  7 years, 5 months, 11 days, 9 hours, 4 minutes, 19 seconds
Difference in times:  1 years, 1 months, 25 days, 3 hours, 30 minutes, 38 seconds
Ship Length:  8.660254038  meters
Ship Mass:  11.54700538  tons
```

The `--meterspersec` option lets you specify speeds in meters per second (m/s) instead. So, for example, if you want to find out how long it would take for Voyager 1 to reach Proxima Centauri (if it was going that way, which it isn't), you could do:
```
~/wunderhund/timedil(master*) » ./timedil.py -ms 17000 -l 4.3                           
Lightyears to travel:  4.3
Speed in m/s:  17,000 m/s
Percent of c:  0.005670589618 %
Lorentz Factor:  1.0000000016077794651181420704233460128307342529296875
Observer Time:  75,829 years, 10 months, 8 days, 15 hours, 45 minutes, 16 seconds
Ship Time:  75,829 years, 10 months, 8 days, 14 hours, 38 minutes, 36 seconds
Difference in times:  0 years, 0 months, 0 days, 1 hours, 3 minutes, 6 seconds
Ship Length:  9.999999984  meters
Ship Mass:  10.00000002  tons
```

The other options should be mostly self-explanatory:
`--lightyears` lets you specify how long a trip you are going on; this allows calculating the observer time and ship time for the trip.
`--shiplength` lets you specify a length of a ship (length being the dimension in the direction of travel) to see how the length of the ship would change from the point of view of the observer.
`--precision` lets you change the precision of the floating-point variables. This version uses the `decimal.Decimal` type for these calculations (described [here](https://docs.python.org/2/library/decimal.html))

I added a conditional to handle the special case of _c_=1, because otherwise the `decimal.Decimal` type will try to do the math for it to the limits of its precision, producing inaccurate results. This conditional produces results like:
```
~/wunderhund/timedil(master*) » ./timedil.py -s 1 -l 4.3                                
Lightyears to travel:  4.3
Speed in m/s:  299,792,458 m/s
Percent of c:  100 %
Lorentz Factor:  Infinity
Observer Time:  4 years, 3 months, 18 days, 6 hours, 17 minutes, 28 seconds
Ship Time:  0 years, 0 months, 0 days, 0 hours, 0 minutes, 0 seconds
Difference in times:  4 years, 3 months, 18 days, 6 hours, 17 minutes, 28 seconds
Ship Length:  0  meters
Ship Mass:  Infinity  tons
```

## Superluminal velocities

This script allows for the computation of faster-than-light values. This requires a small change in the Lorentz equation, taking the absolute value of the `(1-ß)` component of the denominator. This prevents higher-than-1 values of _c_ from causing the denominator to turn out negative, which leads to imaginary numbers.

In the real universe (so far as we know), travel faster than the speed of light is impossible, as reflected by the imaginary numbers when the equation is completed correctly. However, playing around with this equation shows that taking the aboslute value of this component results in all of the same values at sub-luminal speeds, while creating a concept of "reverse dilation" for superlumnal velocities.

In this setup, ships traveling at faster-than-light speeds continue to reach their destination in less and less time (from an outside observer's point of view), but make up for that speed by having more time take place on the ship. So, for example, if you were to travel to Proxima Centauri 4.3 light-years away at the equivalent of Warp 9 (1516 _c_):
```
~/wunderhund/timedil(master*) » ./timedil.py -s 1516 -l 4.3                             
Lightyears to travel:  4.3
Speed in m/s:  4.544853663E+11 m/s
Percent of c:  151600.0000 %
Lorentz Factor:  0.0006596307503770322371028367314238494145683944225311279296875
Observer Time:  0 years, 0 months, 1 days, 0 hours, 51 minutes, 48 seconds
Ship Time:  4 years, 3 months, 18 days, 6 hours, 16 minutes, 59 seconds
Difference in times:  4 years, 3 months, 17 days, 5 hours, 25 minutes, 10 seconds
Ship Length:  15159.99670  meters
Ship Mass:  0.006596307504  tons
```

Interestingly, the multiple of _c_ where the ship and observer times match up is precisely at the mathematical constant _e_, which is the square root of 2: `1.414213562373095`:
```
~/wunderhund/timedil(master*) » ./timedil.py -s 1.414213562373095 -l 4.3                
Lightyears to travel:  4.3
Speed in m/s:  423,970,560.0 m/s
Percent of c:  141.4213562 %
Lorentz Factor:  1.0000000002634952256386213775840587913990020751953125
Observer Time:  3 years, 0 months, 14 days, 19 hours, 32 minutes, 2 seconds
Ship Time:  3 years, 0 months, 14 days, 19 hours, 32 minutes, 2 seconds
Difference in times:  0 years, 0 months, 0 days, 0 hours, 0 minutes, 0 seconds
Ship Length:  9.999999997  meters
Ship Mass:  10.00000000  tons
```

**Please note:** Values for speeds higher than the speed of light should be considered preliminary, pending further investigation.
