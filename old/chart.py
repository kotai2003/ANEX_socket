# Fixing the indentation error and continuing the flowchart creation
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def create_flowchart():
    fig, ax = plt.subplots(figsize=(12, 12))

    # Draw rectangles
    start = mpatches.Rectangle([0.2, 0.9], 0.6, 0.05, color="green", ec="black")
    connect = mpatches.Rectangle([0.2, 0.82], 0.6, 0.05, color="lightblue", ec="black")
    init = mpatches.Rectangle([0.2, 0.74], 0.6, 0.05, color="lightblue", ec="black")
    loop_start = mpatches.Rectangle([0.2, 0.68], 0.6, 0.05, color="orange", ec="black")
    carry_driver_bit = mpatches.Rectangle([0.2, 0.6], 0.6, 0.05, color="lightblue", ec="black")
    image_capture = mpatches.Rectangle([0.2, 0.52], 0.6, 0.05, color="lightblue", ec="black")
    ai_check = mpatches.Rectangle([0.2, 0.44], 0.6, 0.05, color="lightblue", ec="black")
    rotate = mpatches.Rectangle([0.2, 0.36], 0.6, 0.05, color="lightblue", ec="black")
    reverse = mpatches.Rectangle([0.2, 0.28], 0.6, 0.05, color="lightblue", ec="black")
    end = mpatches.Rectangle([0.2, 0.1], 0.6, 0.05, color="red", ec="black")

    # Add rectangles to the plot
    ax.add_patch(start)
    ax.add_patch(connect)
    ax.add_patch(init)
    ax.add_patch(loop_start)
    ax.add_patch(carry_driver_bit)
    ax.add_patch(image_capture)
    ax.add_patch(ai_check)
    ax.add_patch(rotate)
    ax.add_patch(reverse)
    ax.add_patch(end)

    # Add text to rectangles
    ax.text(0.5, 0.925, 'Start', ha='center', va='center', fontsize=12, color="white")
    ax.text(0.5, 0.845, 'Connect to server', ha='center', va='center', fontsize=12, color="black")
    ax.text(0.5, 0.765, 'Initialize', ha='center', va='center', fontsize=12, color="black")
    ax.text(0.5, 0.705, 'Begin Loop', ha='center', va='center', fontsize=12, color="black")
    ax.text(0.5, 0.625, 'Carry Driver Bit', ha='center', va='center', fontsize=12, color="black")
    ax.text(0.5, 0.545, 'Capture Image', ha='center', va='center', fontsize=12, color="black")
    ax.text(0.5, 0.465, 'AI Anomaly Detection', ha='center', va='center', fontsize=12, color="black")
    ax.text(0.5, 0.385, 'Rotate', ha='center', va='center', fontsize=12, color="black")
    ax.text(0.5, 0.305, 'Reverse', ha='center', va='center', fontsize=12, color="black")
    ax.text(0.5, 0.125, 'End', ha='center', va='center', fontsize=12, color="white")

    # Draw arrows
    arrow_style = mpatches.ArrowStyle.CurveFilledB(head_length=1.2, head_width=0.5)
    ax.annotate('', xy=(0.5, 0.82), xytext=(0.5, 0.87),
                arrowprops=dict(arrowstyle=arrow_style, color="black"))
    ax.annotate('', xy=(0.5, 0.74), xytext=(0.5, 0.79),
                arrowprops=dict(arrowstyle=arrow_style, color="black"))
    ax.annotate('', xy=(0.5, 0.68), xytext=(0.5, 0.73),
                arrowprops=dict(arrowstyle=arrow_style, color="black"))
    ax.annotate('', xy=(0.5, 0.6), xytext=(0.5, 0.65),
                arrowprops=dict(arrowstyle=arrow_style, color="black"))
    ax.annotate('', xy=(0.5, 0.52), xytext=(0.5, 0.57),
                arrowprops=dict(arrowstyle=arrow_style, color="black"))

    # Continuing with the creation of the flowchart

    ax.annotate('', xy=(0.5, 0.52), xytext=(0.5, 0.57),
                arrowprops=dict(arrowstyle=arrow_style, color="black"))
    ax.annotate('', xy=(0.5, 0.44), xytext=(0.5, 0.49),
                arrowprops=dict(arrowstyle=arrow_style, color="black"))
    ax.annotate('', xy=(0.5, 0.36), xytext=(0.5, 0.41),
                arrowprops=dict(arrowstyle=arrow_style, color="black"))
    ax.annotate('', xy=(0.5, 0.28), xytext=(0.5, 0.33),
                arrowprops=dict(arrowstyle=arrow_style, color="black"))
    ax.annotate('', xy=(0.5, 0.1), xytext=(0.5, 0.15),
                arrowprops=dict(arrowstyle=arrow_style, color="black"))

    # Set limits and hide axes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Save the figure
    chart_path = "client_main_loop_flowchart.png"
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.show()

    return chart_path

flowchart_path = create_flowchart()

