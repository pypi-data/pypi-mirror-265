#!/usr/bin/env python
# coding: utf-8

# This librarys purpose is to make 3d VISUALIZATION IMPORTS MUCH EASIER AND CONVINIENT ALONG WITH FITTING DATA INTO THE GRAPHS.

# # Note on Utilizing GPT for Code Optimization
# In developing this project, I leveraged GPT, an AI by OpenAI, to assist with code optimization. The process was highly interactive:
# 
# Direct Input: My queries and directions shaped GPT's outputs, ensuring the solutions were tailored to our specific project needs.
# 
# Selective Integration: I critically evaluated GPT's suggestions, integrating them with significant modifications for optimization, thereby maintaining the project's unique character.
# 
# Originality: The core ideas and logic remain my original work. GPT's role was purely assistive, enhancing the project without compromising its originality.
# 
# Ethical Use: This transparent acknowledgment underlines my commitment to ethical practices. The collaboration with GPT was guided by principles, ensuring the work remains free from plagiarism and represents a blend of human ingenuity and AI efficiency.

# In[2]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generating sample data
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x, y)
z = np.sin(np.sqrt(x**2 + y**2))


# ## 3d SCATTER PLOT

# In[3]:


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z)
ax.set_title('3D Scatter Plot')
plt.show()


# ## 3D Line Plot

# In[4]:


theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z_line = np.linspace(-2, 2, 100)
r = z_line**2 + 2
x_line = r * np.sin(theta)
y_line = r * np.cos(theta)
z_line = r * np.tan(theta)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_line, y_line, z_line)
ax.set_title('3D Line Plot')
ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')

# Adjust the viewing angle to improve visibility of the z-axis label
ax.view_init(elev=10, azim=-40)
plt.show()


#  # 3D Surface Plot

# In[7]:


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis')
ax.set_title('3D Surface Plot')
plt.show()


# # 3D Wireframe Plot

# In[6]:


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(x, y, z)
ax.set_title('3D Wireframe Plot')
plt.show()


# # 3D Contour Plot
# 

# In[8]:


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.contour3D(x, y, z, 50, cmap='binary')
ax.set_title('3D Contour Plot')
plt.show()


# # Classes to call for visualization

# ## class Base3DVisualization

# In[10]:


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Base3DVisualization:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def set_labels(self, xlabel='x axis', ylabel='y axis', zlabel='z axis'):
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_zlabel(zlabel)

    def set_view_angle(self, elev=20, azim=-35):
        self.ax.view_init(elev=elev, azim=azim)

    def show(self):
        plt.show()


# ## ScatterPlot3D

# In[16]:


class ScatterPlot3D(Base3DVisualization):
    def plot(self):
        self.ax.scatter(self.x, self.y, self.z)
        self.set_labels()

    def display_plot(self, xlabel='X Label', ylabel='Y Label', zlabel='Z Label', elev=30, azim=120):
        self.plot()  # Call the plot method to scatter plot the data
        self.set_labels(xlabel, ylabel, zlabel)  # Set custom labels
        self.set_view_angle(elev, azim)  # Set a custom view angle
        self.show()  # Show the plot


# ## LinePlot3D

# In[17]:


class LinePlot3D(Base3DVisualization):
    def plot(self):
        self.ax.plot(self.x, self.y, self.z)
        self.set_labels()


# ## SurfacePlot3D

# In[19]:


class SurfacePlot3D(Base3DVisualization):
    def __init__(self, x, y, z_function):
        super().__init__(x, y, None)
        self.X, self.Y = np.meshgrid(x, y)
        self.Z = z_function(self.X, self.Y)

    def plot(self, cmap='viridis'):
        self.ax.plot_surface(self.X, self.Y, self.Z, cmap=cmap)
        self.set_labels()


# ## WireframePlot3D

# In[23]:


class WireframePlot3D(Base3DVisualization):
    def __init__(self, x, y, z_function):
        super().__init__(x, y, None)
        self.X, self.Y = np.meshgrid(x, y)
        self.Z = z_function(self.X, self.Y)

    def plot(self):
        self.ax.plot_wireframe(self.X, self.Y, self.Z)
        self.set_labels()


# ## ContourPlot3D

# In[25]:


class ContourPlot3D(Base3DVisualization):
    def __init__(self, x, y, z_function):
        super().__init__(x, y, None)
        self.X, self.Y = np.meshgrid(x, y)
        self.Z = z_function(self.X, self.Y)

    def plot(self, cmap='viridis'):
        self.ax.contour3D(self.X, self.Y, self.Z, 50, cmap=cmap)
        self.set_labels()


# In[26]:


# Example usage for a surface plot:
if __name__ == '__main__':
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    z_function = lambda x, y: np.sin(np.sqrt(x**2 + y**2))
    surface_plot = SurfacePlot3D(x, y, z_function)
    surface_plot.plot(cmap='viridis')
    surface_plot.set_view_angle(elev=30, azim=45)
    surface_plot.show()

