import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np

class ImageEncryptor:
    def __init__(self, root):
        self.root = root
        root.title("Image Encryption")
        root.geometry("900x600")
        root.configure(bg="#1a1a2e")
        
        self.img = None
        self.enc_img = None
        
        # Controls
        frame = tk.Frame(root, bg="#1a1a2e")
        frame.pack(pady=10)
        
        tk.Label(frame, text="Method:", bg="#1a1a2e", fg="white").grid(row=0, column=0, padx=5)
        self.method = ttk.Combobox(frame, values=["xor", "swap", "negate", "add", "multiply"], width=10, state="readonly")
        self.method.set("xor")
        self.method.grid(row=0, column=1, padx=5)
        
        tk.Label(frame, text="Key:", bg="#1a1a2e", fg="white").grid(row=0, column=2, padx=5)
        self.key = tk.Entry(frame, width=10)
        self.key.insert(0, "123")
        self.key.grid(row=0, column=3, padx=5)
        
        tk.Button(frame, text="Upload", command=self.upload, bg="#0f3460", fg="white").grid(row=0, column=4, padx=5)
        tk.Button(frame, text="Encrypt", command=self.encrypt, bg="#16213e", fg="white").grid(row=0, column=5, padx=5)
        tk.Button(frame, text="Decrypt", command=self.decrypt, bg="#533483", fg="white").grid(row=0, column=6, padx=5)
        tk.Button(frame, text="Save", command=self.save, bg="#e94560", fg="white").grid(row=0, column=7, padx=5)
        
        # Canvas
        canvas_frame = tk.Frame(root, bg="#1a1a2e")
        canvas_frame.pack(fill="both", expand=True, padx=10)
        
        self.canvas1 = tk.Canvas(canvas_frame, bg="#0f3460", width=400, height=400)
        self.canvas1.pack(side="left", padx=5)
        
        self.canvas2 = tk.Canvas(canvas_frame, bg="#0f3460", width=400, height=400)
        self.canvas2.pack(side="right", padx=5)
    
    def upload(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.img = np.array(Image.open(path))
            self.show(Image.fromarray(self.img), self.canvas1)
    
    def show(self, img, canvas):
        img.thumbnail((380, 380))
        photo = ImageTk.PhotoImage(img)
        canvas.delete("all")
        canvas.create_image(200, 200, image=photo)
        canvas.image = photo
    
    def process(self, arr, encrypt=True):
        method = self.method.get()
        k = self.key.get()
        result = arr.copy()
        
        if method == "xor":
            result[:, :, :3] ^= int(k) % 256
        elif method == "swap":
            result[:, :, [0, 1, 2]] = arr[:, :, [2, 0, 1]]
        elif method == "negate":
            result[:, :, :3] = 255 - arr[:, :, :3]
        elif method == "add":
            val = int(k) if encrypt else -int(k)
            result[:, :, :3] = (arr[:, :, :3].astype(np.int16) + val) % 256
        elif method == "multiply":
            factor = float(k) if encrypt else 1/float(k)
            result[:, :, :3] = np.clip(arr[:, :, :3] * factor, 0, 255)
        
        return result.astype(np.uint8)
    
    def encrypt(self):
        if self.img is None:
            messagebox.showwarning("Warning", "Upload image first!")
            return
        self.enc_img = self.process(self.img, True)
        self.show(Image.fromarray(self.enc_img), self.canvas2)
    
    def decrypt(self):
        if self.enc_img is None:
            messagebox.showwarning("Warning", "Encrypt image first!")
            return
        dec = self.process(self.enc_img, False)
        self.show(Image.fromarray(dec), self.canvas2)
    
    def save(self):
        if self.enc_img is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if path:
            Image.fromarray(self.enc_img).save(path)

if __name__ == "__main__":
    root = tk.Tk()
    ImageEncryptor(root)
    root.mainloop()