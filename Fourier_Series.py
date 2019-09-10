from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("ggplot")


# plots square wave given in problem (can change frequency from terminal)
def plot_sq_graph(fund_per, min_time, max_time):
    fund_per = 2 * np.pi / fund_per
    t = np.linspace(min_time, max_time, 10000, endpoint=False)
    plt.plot(t, .5 * signal.square(fund_per * t + np.pi / 2) + .5, linewidth=2, label='Square wave')


# plots sawtooth wave
def plot_st_graph(fund_per, min_time, max_time):
    t = np.linspace(min_time-(fund_per/2), max_time-(fund_per/2), 10000, endpoint=False)
    plt.plot(t+(fund_per/2), signal.sawtooth(2 * np.pi / fund_per * t), linewidth=2, label='Sawtooth wave')


# Outputs X_n of given fourier coefficients
def print_xn(f_coe, fund_per, min_time, max_time):
    count = 0
    count_two = 0
    theta = (2 * np.pi / fund_per)
    # To get X_n(t), we must repeat the sum for every t
    for i in range(int(min_time), int(max_time + 1)):
        print("For t = " + str(i))
        x_n_real = 0
        x_n_imag = 0
        for j in range(int(min_time), int(max_time + 1)):
            x_n_real += f_coe[count] * np.cos(theta * i * j)
            x_n_imag += f_coe[count] * np.sin(theta * i * j)
            count += 1
        x_n = complex(x_n_real, x_n_imag)
        print(x_n)
        count = 0
        count_two += 1


# Calculates a_k coefficient
def a_k(n, choice):
    # for square wave
    if choice == 0:
        return .5 * np.sinc(n / 2)
    # For saw wave
    if choice == 1:
        if n == 0:
            return 0
        else:
            return (1/(n*np.pi))*(np.cos((n*np.pi)) - 2*np.sin((n*np.pi))/(n*np.pi))


# gets points for fourier representation and plots
def get_fourier(min_time, max_time, n_amount, fund_per, choice):
    # if you want faster run time (less accurate), lower the number below this comment
    intervals = int((abs(min_time) + abs(max_time)) * 1000)
    t = np.linspace(min_time, max_time, intervals, endpoint=False)
    f = []
    for x in t:
        x_n_real = 0
        x_n_imag = 0
        # gets points for fourier plot (summation)
        for n in range(-n_amount, n_amount+1):
            theta = (2 * np.pi / fund_per) * x * n
            x_n_real += a_k(n, int(choice)) * np.cos(theta)
            x_n_imag -= a_k(n, int(choice)) * np.sin(theta)
        f.append(x_n_real + x_n_imag)
    plt.plot(t, f, linewidth=1, label='N = ' + str(n_amount))


# Executes all commands needed for assignment
def main():
    # Takes user input
    fund_per = abs(float(input("Enter fundamental period, T: ")))
    min_time = float(input("Enter minimum time you want graphed: "))
    max_time = float(input("Enter maximum time you want graphed: "))

    # Asks user what graph they want to plot
    choose_graph = 2
    while choose_graph > 1 or choose_graph < 0:
        choose_graph = int(input("Type 0 for square wave, 1 for sawtooth: "))
        if choose_graph == 0:
            plot_sq_graph(fund_per, min_time, max_time)
        elif choose_graph == 1:
            plot_st_graph(fund_per, min_time, max_time)

    # Asks user if they are giving fourier coefficients
    input_coe = 2
    while input_coe > 1 or input_coe < 0:
        input_coe = int(input("Are you giving fourier coefficients? Type 1 or 0 "))
    if input_coe == 1:
        f_coe = []
        for i in range(int(min_time), int(max_time + 1)):
            temp_var = complex(input("Enter Fourier series coefficients a_" + str(i) + ": "))
            f_coe.append(temp_var)
        print_xn(f_coe, fund_per, min_time, max_time)

    # plots fourier series representation(s)
    n_amount = [3, 5, 11, 32, 100]
    length = len(n_amount)
    for i in range(length):
        get_fourier(min_time, max_time, n_amount[i], fund_per, choose_graph)


main()
plt.xlabel('Time')
plt.ylabel('Fourier Values ($X_N$(t))')
plt.title('Fourier Series Representation')
plt.legend()
plt.show()

