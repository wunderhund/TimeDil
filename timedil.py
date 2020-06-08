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

    time_string = (
        f"{int(years):,} years, "
        f"{int(months)} months, " 
        f"{int(days)} days, " 
        f"{int(hours)} hours, " 
        f"{int(minutes)} minutes, " 
        f"{int(seconds)} seconds"
    )
    return time_string


def main():
    """Main Fuction"""
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--speed', type=Decimal,
                       help="Speed expressed as a multiple of the speed of light. \
                       Speed of light = 1")
    group.add_argument('-ms', '--meterspersec', type=Decimal,
                       help="Speed expressed in meters per second")
    parser.add_argument('-l', '--lightyears', type=Decimal, default=1,
                        help='Light-years to travel. Defaults to 1.')
    parser.add_argument('-sl', '--shiplength', type=Decimal, default=10,
                        help='Length of your ship in meters. Defaults to 10.')
    parser.add_argument('-p', '--precision', type=int, default=6,
                        help="Number of decimal places. Defaults to 6.")
    parser.add_argument('-m', '--mass', type=Decimal, default=10000,
                        help="Mass of your ship in kg. Defaults to 10000.")
    parser.add_argument('-t', '--time', type=Decimal, default=0.5,
                        help="Proportion of trip spent accelerating (0-1). Defaults to 0.5")
    args = parser.parse_args()

    if not args.speed and not args.meterspersec:
        print("Must include at least one of --speed or --meterspersec!")
        parser.print_help()
        exit()

    # Constants
    c = 299792458  # The speed of light in meters/sec
    c2 = c ** 2  # The speed of light, squared
    getcontext().prec = args.precision

    # Calculate time of trip (in years) for non-traveling observer
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
        ship_mass = args.mass * gamma
        kinetic_energy_classic = Decimal('Infinity')
        kinetic_energy_relative = Decimal('Infinity')
    else:
        gamma = Decimal(1 / ((abs(1 - B)) ** 0.5))
        ship_time = Decimal(obs_time / gamma)
        ship_length = args.shiplength / gamma
        ship_mass = args.mass * gamma
        kinetic_energy_classic = Decimal(0.5) * args.mass * v2
        kinetic_energy_relative = (args.mass * gamma * c2) - (args.mass * c2)

    ship_energy = ship_mass * c2  # E=mc^2 

    time_diff = abs(obs_time - ship_time)

    output_items = [
        f"-----------------------------------------",
        f"Lightyears to travel: {args.lightyears}",
        f"Speed in m/s: {v:,} m/s",
        f"Percent of c: {v / c*100}%",
        f"Lorentz Factor: {Decimal(gamma)}",
        f"Observer Time: {time_breakdown(obs_time)}",
        f"Ship Time: {time_breakdown(ship_time)}",
        f"Difference in times: {time_breakdown(time_diff)}",
        f"Ship Length: {ship_length} meters",
        f"Ship Mass: {ship_mass} kg",
        f"Ship Mass Energy Equivalent: {ship_energy} joules",
        f"Kinetic Energy Required (Classic): {kinetic_energy_classic} joules",
        f"Kinetic Energy Required (Relativity): {kinetic_energy_relative} joules",
    ]

    print("\n".join(output_items))

if __name__ == "__main__":
    main()
