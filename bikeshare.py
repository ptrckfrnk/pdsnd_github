import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while (True):
        city = input('You can choose between Chicago, New York City or Washington.\nPlease type in the city which you want to explore: ').lower()
        print()

        if city in CITY_DATA.keys():
            break
        else:
            continue


    # TO DO: get user input for month (all, january, february, ... , june)

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

    while (True):
        month = input('If you want to filter the results by month, type in the month (e.g. "January", "July", "October").\nIn case you want to see all the months, type in "all": ').lower()
        print()

        if month in months:
            break
        else:
            continue


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while (True):
        day = input('Now you can decide if you want to filter by a specific day (e.g. "Monday", "Thurday", "Saturday").\nIf so, type in the day. Othewise type in "all": ').lower()
        print()

        if day in days:
            break
        else:
            continue


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()      # IMPORTANT: instead of 'day_name()', method 'weekday_name' was used for prject submission, because based on older version of Pandas
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

    popular_month_index = df['month'].mode()[0]

    popular_month = months[popular_month_index - 1]

    print('The most common month is:', popular_month.title(), '\n')


    # TO DO: display the most common day of week

    print('The most common day of the week is:', df['day_of_week'].mode()[0], '\n')


    # TO DO: display the most common start hour

    print('The most common start hour is:', df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    print('The most common start station is:', df['Start Station'].mode()[0], '\n')


    # TO DO: display most commonly used end station

    print('The most common end station is:', df['End Station'].mode()[0], '\n')


    # TO DO: display most frequent combination of start station and end station trip

    df['Station Combination'] = df['Start Station'] + ' to ' + df['End Station']

    print('The most common station combination is:', df['Station Combination'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    total_time = df['Trip Duration'].sum()

    print("The total travel time is {} seconds, which equals to {:.2f} minutes, {:.2f} hours or {:.2f} days.\n".format(total_time, total_time / 60, total_time / 3600, total_time / 86400))


    # TO DO: display mean travel time

    mean_time = df['Trip Duration'].mean()

    print("The mean travel time is {} seconds, which equals to {:.2f} minutes.".format(mean_time, mean_time / 60))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    data = df.groupby(['User Type'])['Start Time'].count()

    type_count = len(data.index)

    print("There are {} types of customers:\n".format(type_count))

    for i in range(type_count):
        print("{}. '{}', Count: {}".format(i+1, data.index[i], data[i]))

    print()


    # TO DO: Display counts of gender

    if 'Gender' in df.columns:
        data = df.groupby(['Gender'])['Start Time'].count()

        type_count = len(data.index)

        print("Counts of gender:\n")

        for i in range(type_count):
            print("{}: {}".format(data.index[i], data[i]))

        print()


    # TO DO: Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        print("Stats about birth years:\n")

        print("Earliest year of birth:", int(df['Birth Year'].min()))
        print("Most recent year of birth:", int(df['Birth Year'].max()))
        print("Most common year of birth:", int(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Display 5 rows of data until the user stops."""

    print("Displaying first 5 rows...\n")

    x = True
    start = 0
    stop = 5

    while(x):
        x = False

        print(df[start:stop], '\n')

        y = input("Would you like to display more? Enter 'yes' or 'no':\n")

        if y.lower() == "yes":
            x = True
            start += 5
            stop += 5
            print()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
