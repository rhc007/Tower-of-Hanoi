import streamlit as st
import plotly.graph_objects as go

# Function to print the towers' state in a textual format
def print_towers(towers, n, move_count):
    lines = []
    lines.append(f"Move: {move_count}")
    for level in range(n, 0, -1):
        line = ""
        for tower in towers:
            if len(tower) >= level:
                line += f"{tower[level - 1]:^5} "
            else:
                line += "  |  "
        lines.append(line)
    lines.append("----- " * 3)
    lines.append("  A    B    C")
    return "\n".join(lines)

# Function to move a disk from one tower to another
def move_disk(towers, from_tower, to_tower, move_count):
    disk = towers[from_tower].pop()
    towers[to_tower].append(disk)
    move_count += 1
    return move_count, towers

# Recursive function to solve the Tower of Hanoi problem
def tower_of_hanoi(n, source, target, auxiliary, towers, move_count, steps):
    if n == 1:
        move_count, towers = move_disk(towers, source, target, move_count)
        steps.append((move_count, [tower.copy() for tower in towers]))
        return move_count, towers

    move_count, towers = tower_of_hanoi(n-1, source, auxiliary, target, towers, move_count, steps)
    move_count, towers = move_disk(towers, source, target, move_count)
    steps.append((move_count, [tower.copy() for tower in towers]))
    move_count, towers = tower_of_hanoi(n-1, auxiliary, target, source, towers, move_count, steps)

    return move_count, towers

# Function to plot the towers' state using Plotly
def plot_towers(towers, n, move_count):
    fig = go.Figure()

    # Define positions for each tower
    tower_positions = [0, 1, 2]
    
    # Plot vertical lines for towers
    for pos in tower_positions:
        fig.add_trace(go.Scatter(
            x=[pos] * 2,
            y=[-1, n],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False
        ))

    # Plot the disks on the towers
    for i, tower in enumerate(towers):
        sizes = [disk * 10 for disk in tower]  # Scale the disk sizes
        positions = list(range(len(tower)))  # Position disks from bottom to top
        fig.add_trace(go.Scatter(
            x=[i] * len(tower),
            y=positions,
            mode='markers+text',
            text=[str(disk) for disk in tower],
            textposition='top center',
            marker=dict(
                size=sizes,  # Adjust the size of the markers
                color='rgba(219, 64, 82, 0.8)',
                line=dict(width=2, color='rgba(219, 64, 82, 0.8)')
            ),
            name=f'Tower {chr(65 + i)}',  # Optional name, will not show in legend
            showlegend=False  # Hide legend for each trace
        ))

    fig.update_layout(
        title=f'Tower of Hanoi - Move {move_count}',
        xaxis=dict(
            title='Towers',
            tickvals=[0, 1, 2],
            ticktext=['A', 'B', 'C'],
            range=[-0.5, 2.5]  # Ensure there's space around the towers
        ),
        yaxis=dict(
            title='Disk Position',
            range=[-1, n + 1],
            tickvals=list(range(n)),
            ticktext=[str(i) for i in range(n-1, -1, -1)]
        ),
        width=800,  # Increase width of the figure
        height=600,  # Increase height of the figure
        showlegend=False  # Ensure legend is hidden for the entire figure
    )
    return fig

# Streamlit interface
st.title('Tower of Hanoi Solver')

# Input to select the number of disks
n = st.number_input("Enter the number of disks:", min_value=1, max_value=10, value=3)

if st.button("Solve"):
    towers = [list(range(n, 0, -1)), [], []]  # Initial state of the towers
    move_count = 0
    steps = []

    steps.append((move_count, [tower.copy() for tower in towers]))

    # Solve the Tower of Hanoi problem
    move_count, towers = tower_of_hanoi(n, 0, 2, 1, towers, move_count, steps)

    st.write(f"Total moves: {move_count}")

    # Display each move and the state of the towers
    for move, towers_state in steps:
        fig = plot_towers(towers_state, n, move)
        st.plotly_chart(fig)
