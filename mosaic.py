
import matplotlib.pyplot as plt

class PointCollection:
    def __init__(self):
        self.points = []  # List of (x, y) points
        self.ax = None  # Matplotlib axis, initially None
        self.box = None  # Bounding rectangle, initially None

    def add_point(self, x, y):
        """Add a point to the collection and invalidate the bounding box."""
        self.points.append((x, y))
        self.box = None  # Invalidate the bounding box

    def remove_point(self, x, y):
        """Remove a point from the collection and invalidate the bounding box."""
        self.points = [point for point in self.points if point != (x, y)]
        self.box = None  # Invalidate the bounding box

    def remove_point_by_index(self, index):
        """Remove a point by its index in the list and invalidate the bounding box."""
        if 0 <= index < len(self.points):
            self.points.pop(index)
            self.box = None  # Invalidate the bounding box
        else:
            raise IndexError("Index out of range")

    def write_to_file(self, file):
        """Write the points to an already open file, with context strings."""
        file.write("Mosaic Points:\n")  # Write the starting phrase
        for point in self.points:
            file.write(f"{point[0]},{point[1]}\n")
        file.write("End of points.\n")  # Write the ending phrase

    def read_from_file(self, file):
        """Read points from an already open file, checking for context strings."""
        self.points = []  # Clear existing points
        self.box = None  # Invalidate the bounding box

        # Check for the starting phrase
        first_line = file.readline()
        if first_line != "Mosaic Points:\n":
            raise ValueError("File does not start with 'Mosaic Points:'")

        # Read points until the ending phrase is encountered
        for line in file:
            if line == "End of points.\n":
                break  # Stop reading when the ending phrase is found
            x, y = map(float, line.strip().split(','))
            self.points.append((x, y))

    def __str__(self):
        """Return a string representation of the points."""
        return "\n".join(f"({x}, {y})" for x, y in self.points)

    def get_bounding_rectangle(self):
        """Return the bounding rectangle of all points as (x_min, y_min, x_max, y_max)."""
        if self.box is not None:
            return self.box  # Return cached bounding box

        if not self.points:
            raise ValueError("No points in the collection")

        # Initialize min and max values with the first point
        x_min = x_max = self.points[0][0]
        y_min = y_max = self.points[0][1]

        # Find the min and max x and y values
        for x, y in self.points:
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y

        # Cache the bounding box
        self.box = (x_min, y_min, x_max, y_max)
        return self.box

    def get_plot(self):
        """Create and return a matplotlib plot with the correct aspect ratio."""
        x_min, y_min, x_max, y_max = self.get_bounding_rectangle()

        # Calculate the aspect ratio
        width = x_max - x_min
        height = y_max - y_min
        aspect_ratio = width / height

        # Create a figure with the same aspect ratio as the bounding rectangle
        fig, ax = plt.subplots(figsize=(8, 8 / aspect_ratio))

        # Set the limits of the plot to match the bounding rectangle
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        # Remove axes and labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_axis_off()

        # Ensure the aspect ratio is correct
        ax.set_aspect('equal', adjustable='box')

        # Store the axis for later use
        self.ax = ax

        return ax

    def on_click(self, event):
        """Handle mouse click events and print the coordinates of the clicked point."""
        if event.inaxes == self.ax:  # Check if the click is within the plot
            x, y = event.xdata, event.ydata
            print(f"Clicked at: ({x:.2f}, {y:.2f})")

class LineSegmentCollection:
    def __init__(self):
        self.segments = []  # List of tuples (start_index, end_index)

    def add_segment(self, start_index, end_index):
        """Add a line segment defined by the indices of two points."""
        self.segments.append((start_index, end_index))

    def remove_segment(self, start_index, end_index):
        """Remove a line segment defined by the indices of two points."""
        self.segments = [seg for seg in self.segments if seg != (start_index, end_index)]

    def remove_segment_by_index(self, index):
        """Remove a line segment by its index in the list."""
        if 0 <= index < len(self.segments):
            self.segments.pop(index)
        else:
            raise IndexError("Index out of range")

    def write_to_file(self, file):
        """Write the line segments to an already open file, with context strings."""
        file.write("Mosaic Line Segments:\n")  # Write the starting phrase
        for seg in self.segments:
            file.write(f"{seg[0]},{seg[1]}\n")
        file.write("End of line segments.\n")  # Write the ending phrase

    def read_from_file(self, file, points):
        """Read line segments from an already open file, checking for context strings."""
        self.segments = []  # Clear existing segments

        # Check for the starting phrase
        first_line = file.readline()
        if first_line != "Mosaic Line Segments:\n":
            raise ValueError("File does not start with 'Mosaic Line Segments:'")

        # Read segments until the ending phrase is encountered
        for line in file:
            if line == "End of line segments.\n":
                break  # Stop reading when the ending phrase is found
            start_index, end_index = map(int, line.strip().split(','))
            # Validate that the indices are within the bounds of the points list
            if start_index < 0 or start_index >= len(points) or end_index < 0 or end_index >= len(points):
                raise ValueError("Invalid point index in line segment")
            self.segments.append((start_index, end_index))

    def __str__(self):
        """Return a string representation of the line segments."""
        return "\n".join(f"({start}, {end})" for start, end in self.segments)

    def plot_line_segments(self, points, ax):
        """
        Open a graphics window with the same aspect ratio as the bounding rectangle
        of the points and plot all the line segments without axes or labels.

        Args:
            points (PointCollection): A PointCollection object containing the points.
            segments (LineSegmentCollection): A LineSegmentCollection object containing the line segments.
        """
        # Get the bounding rectangle of the points

        # Plot each line segment
        for seg in self.segments:
            start_index, end_index = seg
            x_start, y_start = points.points[start_index]
            x_end, y_end = points.points[end_index]
            ax.plot([x_start, x_end], [y_start, y_end], marker='o', linestyle='-', color='b')


class ShapeCollection:
    def __init__(self):
        self.triangles = []  # List of tuples (seg1_index, seg2_index, seg3_index, (r, g, b))
        self.quadrilaterals = []  # List of tuples (seg1_index, seg2_index, seg3_index, seg4_index, (r, g, b))

    def add_triangle(self, seg1_index, seg2_index, seg3_index, segments, colour):
        """Add a triangle defined by three line segments, validating corner matching."""
        if not self._validate_shape([seg1_index, seg2_index, seg3_index], segments):
            raise ValueError("Invalid triangle: segments do not form a closed shape")
        self.triangles.append((seg1_index, seg2_index, seg3_index, colour))

    def add_quadrilateral(self, seg1_index, seg2_index, seg3_index, seg4_index, segments, colour):
        """Add a quadrilateral defined by four line segments, validating corner matching."""
        if not self._validate_shape([seg1_index, seg2_index, seg3_index, seg4_index], segments):
            raise ValueError("Invalid quadrilateral: segments do not form a closed shape")
        self.quadrilaterals.append((seg1_index, seg2_index, seg3_index, seg4_index, colour))

    def _validate_shape(self, segment_indices, segments):
        """Validate that the segments form a closed shape (corners match)."""
        # Get the segments from their indices
        segment_list = [segments[i] for i in segment_indices]

        # Check that the end of each segment matches the start of the next
        for i in range(len(segment_list)):
            current_seg = segment_list[i]
            next_seg = segment_list[(i + 1) % len(segment_list)]
            if current_seg[1] != next_seg[0]:
                return False
        return True

    def write_to_file(self, file):
        """Write the shapes to an already open file, with context strings."""
        file.write("Mosaic Shapes:\n")  # Write the starting phrase
        # Write triangles
        file.write("Triangles:\n")
        for triangle in self.triangles:
            seg1, seg2, seg3, (r, g, b) = triangle
            file.write(f"{seg1},{seg2},{seg3},{r},{g},{b}\n")
        # Write quadrilaterals
        file.write("Quadrilaterals:\n")
        for quad in self.quadrilaterals:
            seg1, seg2, seg3, seg4, (r, g, b) = quad
            file.write(f"{seg1},{seg2},{seg3},{seg4},{r},{g},{b}\n")
        file.write("End of shapes.\n")  # Write the ending phrase

    def read_from_file(self, file, segments):
        """Read shapes from an already open file, checking for context strings."""
        self.triangles = []  # Clear existing triangles
        self.quadrilaterals = []  # Clear existing quadrilaterals

        # Check for the starting phrase
        first_line = file.readline()
        if first_line != "Mosaic Shapes:\n":
            raise ValueError("File does not start with 'Mosaic Shapes:'")

        # Read shapes until the ending phrase is encountered
        current_section = None
        for line in file:
            if line == "End of shapes.\n":
                break  # Stop reading when the ending phrase is found
            elif line == "Triangles:\n":
                current_section = "Triangles"
            elif line == "Quadrilaterals:\n":
                current_section = "Quadrilaterals"
            else:
                if current_section == "Triangles":
                    seg1, seg2, seg3, r, g, b = map(int, line.strip().split(','))
                    self.triangles.append((seg1, seg2, seg3, (r, g, b)))
                elif current_section == "Quadrilaterals":
                    seg1, seg2, seg3, seg4, r, g, b = map(int, line.strip().split(','))
                    self.quadrilaterals.append((seg1, seg2, seg3, seg4, (r, g, b)))

    def __str__(self):
        """Return a string representation of the shapes."""
        result = "Triangles:\n"
        result += "\n".join(f"({seg1}, {seg2}, {seg3}, ({r}, {g}, {b}))" for seg1, seg2, seg3, (r, g, b) in self.triangles)
        result += "\nQuadrilaterals:\n"
        result += "\n".join(f"({seg1}, {seg2}, {seg3}, {seg4}, ({r}, {g}, {b}))" for seg1, seg2, seg3, seg4, (r, g, b) in self.quadrilaterals)
        return result

    def plot_shapes(self, points, segments, ax):
        """Plot triangles and quadrilaterals on the given matplotlib axis."""
        # Plot triangles
        for triangle in self.triangles:
            seg1, seg2, seg3, (r, g, b) = triangle
            # Get the points for each segment
            x1, y1 = points.points[segments.segments[seg1][0]]
            x2, y2 = points.points[segments.segments[seg1][1]]
            x3, y3 = points.points[segments.segments[seg2][1]]
            ax.fill([x1, x2, x3], [y1, y2, y3], color=(r/255, g/255, b/255), alpha=0.5)

        # Plot quadrilaterals
        for quad in self.quadrilaterals:
            seg1, seg2, seg3, seg4, (r, g, b) = quad
            # Get the points for each segment
            x1, y1 = points.points[segments.segments[seg1][0]]
            x2, y2 = points.points[segments.segments[seg1][1]]
            x3, y3 = points.points[segments.segments[seg2][1]]
            x4, y4 = points.points[segments.segments[seg3][1]]
            ax.fill([x1, x2, x3, x4], [y1, y2, y3, y4], color=(r/255, g/255, b/255), alpha=0.5)

if __name__ == "__main__":
    # Create a PointCollection and add points
    points = PointCollection()
    points.add_point(10.0, 20.0)  # Point 0
    points.add_point(5.0, 2.0)  # Point 1
    points.add_point(15.0, 60.0)  # Point 2
    points.add_point(8.0, 12)  # Point 3
    points.add_point(20.0, 20.0)  # Point 4
    points.add_point(27.0, 2.0)  # Point 5
    points.add_point(5.0, 50.0)  # Point 6

    # Create a LineSegmentCollection and add segments
    segments = LineSegmentCollection()
    segments.add_segment(0, 1)  # Segment 0: Point 0 -> Point 1
    segments.add_segment(1, 2)  # Segment 1: Point 1 -> Point 2
    segments.add_segment(2, 0)  # Segment 2: Point 2 -> Point 0
    segments.add_segment(3, 4)  # Segment 3: Point 3 -> Point 4
    segments.add_segment(4, 5)  # Segment 4: Point 4 -> Point 5
    segments.add_segment(5, 6)  # Segment 5: Point 5 -> Point 6
    segments.add_segment(6, 3)  # Segment 6: Point 6 -> Point 3

    # Create a ShapeCollection and add shapes with RGB colours
    shapes = ShapeCollection()
    shapes.add_triangle(0, 1, 2, segments.segments, (255, 0, 0))  # Red triangle
    shapes.add_quadrilateral(3, 4, 5, 6, segments.segments, (0, 0, 255))  # Blue quadrilateral

    # Plot the original data
    ax = points.get_plot()
    segments.plot_line_segments(points, ax)
    shapes.plot_shapes(points, segments, ax)
    plt.title("Mosaic Design")

    # Connect the mouse click event to the on_click method
    plt.connect('button_press_event', points.on_click)

    # Show the plot in a non-blocking way
    plt.show(block=False)

    # Write all data to a file
    with open("mosaic.txt", "w") as file:
        points.write_to_file(file)
        segments.write_to_file(file)
        shapes.write_to_file(file)

    print("Data written to 'mosaic.txt'")

    # Keep the program running to allow interaction with the plot
    print("Click on the plot to get coordinates. Close the plot window to exit.")
    plt.pause(0.1)  # Small pause to ensure the plot window is ready
    while plt.get_fignums():  # Keep running while the plot window is open
        plt.pause(0.1)
