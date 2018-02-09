from time import perf_counter
from operator import itemgetter
import contextlib
import sqlite3
import random

from tabulate import tabulate

from shimcontrol.lib import ADCCommandSet, DACCommandSet


def time_function(times, func, *args, **kwargs):
    start = perf_counter()

    for _ in range(times):
        func(*args, **kwargs)

    end = perf_counter()

    return end - start

def measure_adc_perf(channels):
    calls = 10000

    adc = ADCCommandSet(5)
    adc.from_read(channels)

    time_taken = time_function(calls, adc.execute)

    return (calls, time_taken)

def measure_dac_perf(number_of_channels):
    calls = 1000
    group_calls = 10

    total_time = 0.0
    total_calls = 0

    for _ in range(group_calls):
        dac = DACCommandSet(5)
        dac.from_write([
            (ch, random.randint(0x0000, 0xffff))
            for ch in random.sample(range(40), number_of_channels)
        ])

        time_taken = time_function(calls, dac.execute)

        total_time += time_taken
        total_calls += calls

    return (total_calls, total_time)


def adc_perf_report():
    data = []

    for number_of_channels in range(1, 9):
        channels = list(range(number_of_channels))

        calls, time_taken = measure_adc_perf(channels)

        data.append([
            number_of_channels,
            time_taken / calls / number_of_channels,
            time_taken,
            calls
        ])

    return data

def dac_perf_report():
    data = []

    for number_of_channels in range(1, 41):
        print(number_of_channels)
        calls, time_taken = measure_dac_perf(number_of_channels)

        data.append([
            number_of_channels,
            time_taken / calls / number_of_channels,
            time_taken,
            calls,
        ])

    return data


def print_adc_perf_report():
    data = adc_perf_report()

    print(tabulate(
        data,
        headers=[
            'Número de canais', 'Tempo por canal (s)', 'Tempo (s)', 'Chamadas'
        ],
    ))


def print_dac_perf_report():
    data = dac_perf_report()

    print(tabulate(
        data,
        headers=[
            'Número de canais', 'Tempo por canal (s)', 'Tempo (s)', 'Chamadas'
        ],
    ))

def measure_dac_to_adc_voltage(dac_channels, adc_channels, times):
    if len(dac_channels) != len(adc_channels):
        raise TypeError

    def expected_voltage(code):
        return 4.096 - (2 * 4.096) * (code / float(0xffff))

    conn = sqlite3.connect('shimcontrol-voltages.sqlite3')
    cursor = conn.cursor()

    cursor.execute('''
        create table if not exists voltages (
            dac int,
            adc int,
            code int,
            expected real,
            real real
        )
    ''')

    for _ in range(times):
        dac_codes = [
            random.randint(0x0000, 0xffff)
            for _ in range(len(dac_channels))
        ]

        expected = [expected_voltage(code) for code in dac_codes]

        dacset = DACCommandSet(5)
        dacset.from_write(zip(dac_channels, dac_codes))
        dacset.execute()

        adcset = ADCCommandSet(5)
        adcset.from_read(adc_channels)
        results = adcset.execute()

        results.sort(key=lambda x: adc_channels.index(x[0]))

        diff = [
            expected - real
            for expected, real in zip(expected, map(itemgetter(1), results))
        ]

        for dac, adc, code, exp, real in zip(dac_channels, adc_channels, dac_codes, expected, results):
            cursor.execute(
                'insert into voltages values (?, ?, ?, ?, ?)',
                (dac, adc, code, exp, real[1])
            )
            conn.commit()
