import matplotlib.pyplot as plt

def exportLegend(legend, filename="../img/caption.png"):
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi=400, bbox_inches=bbox)

if __name__ == '__main__':

    colors = []
    label_colors = ["red", "green", "yellow" , "white" , 'undefined']
    f = lambda m,c: plt.plot([],[],marker=m, color=c, ls="none")[0]

    for i in range(5):
        if label_colors[i]=='red':
            colors.append('red')
        elif label_colors[i]=='green':
            colors.append('green')
        elif label_colors[i]=='yellow':
            colors.append('orange')
        elif label_colors[i]=='white':
            colors.append('yellow')
        elif label_colors[i]=='undefined':
            colors.append('grey')

    handles = [f("s", colors[i]) for i in range(len(label_colors))]

    label_colors

    legend = plt.legend(handles, label_colors, loc=5, framealpha=1, frameon=True , mode='expand',ncol=5 , title="Light Color Caption:")

    #legend = plt.legend(handles, label_colors, loc=5, framealpha=1, frameon=True , title="Light Color Caption:")

    exportLegend(legend)