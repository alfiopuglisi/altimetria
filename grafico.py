
import matplotlib.pyplot as plt


#Segment = namedtuple('Segment', 'start end len elev_start elev_gain grade')

def grade_color(grade):
    if grade < 5:
        return 'limegreen'
    if grade < 7:
        return 'dodgerblue'
    if grade < 10:
        return 'yellow'
    return 'red'

def grafico(segments, ymargin=0.1, textmargin=0.01):

    points = []
    for segment in segments:
        x1 = segment.start
        x2 = segment.end
        y1 = segment.elev_start
        y2 = segment.elev_start + segment.elev_gain
        points.append([x1,y1])
        points.append([x2,y2])

    ymin = min([p[1] for p in points])
    ymax = max([p[1] for p in points])
    yptp = ymax-ymin

    ax = plt.gca()

    for segment in segments:
        x1 = segment.start
        x2 = segment.end
        y1 = segment.elev_start
        y2 = segment.elev_start + segment.elev_gain
        ax.fill_between([x1,x2],[y1,y2], color=grade_color(segment.grade))
        ax.plot([x2, x2], [0, y2], linestyle='dashed', linewidth=1, color='black')
        ax.text(x1+(x2-x1)/2, ymin-yptp*0.09, f'{segment.grade:.1f}', horizontalalignment='center')
        if segment is segments[0]:
            valign='top'
        else:
            valign='bottom'
        ax.text(x1, y1+yptp*textmargin, f'{y1:.0f}', rotation=90, verticalalignment=valign, rotation_mode='anchor', color='black')
    ax.text(x2, y2+yptp*textmargin, f'{y1:.0f}', rotation=90, verticalalignment='bottom',rotation_mode='anchor', color='black')

    ax.set_ylim([ymin-yptp*ymargin, ymax+yptp*ymargin])
    ax.set_xlim([0, x2])
    ax.set_xlabel('Distanza (km)')
    ax.set_ylabel('Altitudine metri s.l.m')
    plt.show()
    
