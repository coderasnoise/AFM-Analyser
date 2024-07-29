import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AFMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AFM Image Analyzer")

        self.upload_button = tk.Button(root, text="Resim Yükle", command=self.upload_image)
        self.upload_button.pack()

        self.save_button = tk.Button(root, text="Grafikleri Kaydet", command=self.save_plots, state=tk.DISABLED)
        self.save_button.pack()

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()

        self.image_path = None
        self.figures = []  # List to store figure references
        self.canvases = []  # List to store canvas references

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            self.reset_analysis()
            self.process_image()

    def reset_analysis(self):
        # Clear previous figures and canvases
        for canvas in self.canvases:
            canvas.get_tk_widget().pack_forget()
        self.figures.clear()
        self.canvases.clear()

    def process_image(self):
        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            messagebox.showerror("Error", "Resim dosyası okunamadı!")
            return

        height_data = np.asarray(image, dtype=np.float32)
        height_data = (height_data - height_data.min()) / (height_data.max() - height_data.min())

        Ra = np.mean(np.abs(height_data - np.mean(height_data)))
        Rq = np.sqrt(np.mean((height_data - np.mean(height_data)) ** 2))
        Rz = np.max(height_data) - np.min(height_data)

        messagebox.showinfo("Surface Roughness", f"Ra: {Ra}, Rq: {Rq:}, Rz: {Rz:}")

        self.plot_image(image, "Original AFM Image", 'hot')
        self.plot_image(height_data, "Normalized AFM Image", 'hot')
        self.plot_profile(height_data)
        self.plot_3d_surface(height_data)

        self.save_button.config(state=tk.NORMAL)  # Enable save button

    def plot_image(self, data, title, cmap):
        fig, ax = plt.subplots()
        cax = ax.imshow(data, cmap=cmap)
        ax.set_title(title)
        fig.colorbar(cax)

        self.figures.append(fig)  # Store figure reference

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.canvases.append(canvas)  # Store canvas reference

    def plot_profile(self, height_data):
        profile_line = height_data[height_data.shape[0] // 2, :]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(profile_line)
        ax.set_title('Surface Profile along Centerline')
        ax.set_xlabel('Position')
        ax.set_ylabel('Height (normalized)')
        ax.grid(True)

        self.figures.append(fig)  # Store figure reference

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.canvases.append(canvas)  # Store canvas reference

    def plot_3d_surface(self, height_data):
        X = np.linspace(0, height_data.shape[1], height_data.shape[1])
        Y = np.linspace(0, height_data.shape[0], height_data.shape[0])
        X, Y = np.meshgrid(X, Y)

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, height_data, cmap='hot')

        ax.set_xlabel('X (µm)')
        ax.set_ylabel('Y (µm)')
        ax.set_zlabel('Height (normalized)')
        ax.set_title('3D Surface Topography')

        self.figures.append(fig)  # Store figure reference

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.canvases.append(canvas)  # Store canvas reference

    def save_plots(self):
        directory = filedialog.askdirectory()
        if not directory:
            return

        for i, fig in enumerate(self.figures):
            fig_path = f"{directory}/plot_{i + 1}.png"
            fig.savefig(fig_path)
            messagebox.showinfo("Grafikleri kaydet", f"Grafik {fig_path} adıyla kaydedildi!")


if __name__ == "__main__":
    root = tk.Tk()
    app = AFMApp(root)
    root.mainloop()
