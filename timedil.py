#!/usr/local/bin/python3
"""Script for quick-and-dirty time dilation calculations"""
from argparse import ArgumentParser
from decimal import Decimal, getcontext


def time_breakdown(time_in_years):
    """Function for formatting time nicely"""
    light_seconds = time_in_years * 31556926
    years, year_rem = divmod(light_seconds, 31556926)
    months, month_rem = divmod(year_rem, 2629743)
    days, days_rem = divmod(month_rem, 86400)
    hours, hours_rem = divmod(days_rem, 3600)
    minutes, seconds = divmod(hours_rem, 60)

    time_string = f'{int(years):,}' + " years, " \
                + str(int(months)) + " months, " \
                + str(int(days)) + " days, " \
                + str(int(hours)) + " hours, " \
                + str(int(minutes)) + " minutes, " \
                + str(int(seconds)) + " seconds"
    return time_string


def main():
    """Main Fuction"""
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--speed', type=Decimal,
                       help="Speed expressed as a multiple of the speed of light. \
                       Speed of light = 1")
    group.add_argument('-m', '--meterspersec', type=Decimal,
                       help="Speed expressed in meters per second")
    parser.add_argument('-l', '--lightyears', type=Decimal, default=1,
                        help='Light-years to travel')
    parser.add_argument('-sl', '--shiplength', type=Decimal, default=10,
                        help='Length of your ship in meters')
    parser.add_argument('-p', '--precision', type=int, default=10,
                        help="Number of decimal places. Defaults to 6.")
    args = parser.parse_args()

    if not args.speed and not args.meterspersec:
        print("Must include at least one of --speed or --meterspersec!")
        parser.print_help()
        exit()

    # Constants
    c = 299792458  # The speed of light in meters/sec
    c2 = c ** 2  # The speed of light, squared
    getcontext().prec = args.precision

    if args.speed:
        v = args.speed * c
        obs_time = args.lightyears/args.speed
    elif args.meterspersec:
        v = args.meterspersec
        obs_time = args.lightyears/(args.meterspersec/c)

    v2 = int(v ** 2)
    B = v2/c2

    if args.speed == 1:
        gamma = Decimal('Infinity')
        ship_time = 0
        ship_length = 0
    else:
        gamma = Decimal(1 / (abs(1 - B) ** 0.5))
        ship_time = obs_time / gamma
        ship_length = args.shiplength / gamma

    print("Lightyears to travel: ", args.lightyears)
    print("Speed in m/s: ", f'{v:,}',"m/s")
    print("Percent of c: ", (v / c)*100, "%")
    print("Lorentz Factor: ", Decimal(gamma))
    print("Observer Time: ", time_breakdown(obs_time))
    print("Ship Time: ", time_breakdown(ship_time))
    print("Ship Length: ", ship_length, " meters")


if __name__ == "__main__":
    main()
