import matplotlib.pyplot as plt
import pandas as pd

stilldata = []
onbikedata = []
tiltingdata = []
walkingdata = []
onfootdata = []
invehicledata = []


def main():
    data = pd.read_csv('activitydata.csv', encoding='utf-8').fillna(0)
    timestamp = data['Timeinms'].iloc[0:].values
    activity = data['action'].iloc[0:].values
    confidence = data['confidence'].iloc[0:].values

    ycounter = 0
    for x in activity:
        if x == 'Still':
            stilldata.append(ycounter)
        elif x == 'On Bicycle':
            onbikedata.append(ycounter)
        elif x == 'Tilting':
            tiltingdata.append(ycounter)
        elif x == 'Walking':
            walkingdata.append(ycounter)
        elif x == 'On Foot':
            onfootdata.append(ycounter)
        elif x == 'In vehicle':
            invehicledata.append(ycounter)
        ycounter += 1
    plot(timestamp, confidence)


def plot(time, conf):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title("Activity Data")
    ax.set_xlabel("Time/[Seconds]")
    ax.set_ylabel("Confidence/[0-100]")

    stilltime = []
    stillconf = []
    for x in stilldata:
        stilltime.append((time[x]-time[0])/1000)
        stillconf.append(conf[x])
    ax.scatter(stilltime, stillconf, c='Blue', label='Still', alpha=0.3)

    onbiketime = []
    onbikeconf = []
    for x in onbikedata:
        onbiketime.append((time[x]-time[0])/1000)
        onbikeconf.append(conf[x])
    ax.scatter(onbiketime, onbikeconf, c='Orange', label='On Bike', alpha=0.3)

    tiltingtime = []
    tiltingconf = []
    for x in tiltingdata:
        tiltingtime.append((time[x]-time[0])/1000)
        tiltingconf.append(conf[x])
    ax.scatter(tiltingtime, tiltingconf, c='Grey', label='Tilting', alpha=0.3)

    onfoottime = []
    onfootconf = []
    for x in onfootdata:
        onfoottime.append((time[x]-time[0])/1000)
        onfootconf.append(conf[x])
    ax.scatter(onfoottime, onfootconf, c='Green', label='On Foot', alpha=0.3)

    walkingtime = []
    walkingconf = []
    for x in walkingdata:
        walkingtime.append((time[x]-time[0])/1000)

        walkingconf.append(conf[x])
    ax.scatter(walkingtime, walkingconf, c='Yellow', label='Walking', alpha=0.3)

    invehicletime = []
    invehicleconf = []
    for x in invehicledata:
        invehicletime.append((time[x]-time[0])/1000)
        invehicleconf.append(conf[x])
    ax.scatter(invehicletime, invehicleconf, c='Red', label='In Vehicle', alpha=0.3)

    leg = ax.legend()
    plt.show()


if __name__ == '__main__':
    main()
