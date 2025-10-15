import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import otto_generator

getimage = otto_generator.getimage

class ImageProcessingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("说的道理生成器")
        
        # Initialize parameters
        self.params = {
            'w_proj': 800,
            'h_proj': 600,
            'offset_hor': 0.0,
            'offset_ver': 0.0,
            'scale': 1.2,
            'alpha': 0.0,
            'beta': 0.0,
            'gamma': 0.0
        }
        
        self.skq = 1.0
        
        # File paths
        self.path_img = ""
        self.path_proj = ""
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Configure the main window to be resizable
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main frame grid
        main_frame.columnconfigure(0, weight=1)  # Left panel
        main_frame.columnconfigure(1, weight=0)  # Right panel (preview)
        main_frame.rowconfigure(0, weight=1)
        
        # Left panel (controls)
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(2, weight=1)
        
        # Right panel (preview)
        right_frame = ttk.LabelFrame(main_frame, text="Preview", padding="5")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # File selection
        file_frame = ttk.LabelFrame(left_frame, text="File Paths", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(file_frame, text="输入路径:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.img_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.img_path_var, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_img).grid(row=0, column=2, padx=5)
        
        ttk.Label(file_frame, text="保存路径:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.proj_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.proj_path_var, width=40).grid(row=1, column=1, padx=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_proj).grid(row=1, column=2, padx=5)
        
        # Parameters frame
        params_frame = ttk.LabelFrame(left_frame, text="Parameters", padding="5")
        params_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Parameter controls
        row = 0
        ttk.Label(params_frame, text="投影图像输出尺寸（单位：像素）").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        row+=1
        
        # w_proj
        ttk.Label(params_frame, text="Projection Width (w_proj):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.w_proj_var = tk.IntVar(value=self.params['w_proj'])
        w_proj_scale = ttk.Scale(params_frame, from_=100, to=2000, variable=self.w_proj_var, orient='horizontal', command=self.update_params)
        w_proj_scale.grid(row=row, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        w_proj_entry = ttk.Entry(params_frame, textvariable=self.w_proj_var, width=10)
        w_proj_entry.grid(row=row, column=2, padx=5, pady=2)
        row += 1
        
        # h_proj
        ttk.Label(params_frame, text="Projection Height (h_proj):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.h_proj_var = tk.IntVar(value=self.params['h_proj'])
        h_proj_scale = ttk.Scale(params_frame, from_=100, to=2000, variable=self.h_proj_var, orient='horizontal', command=self.update_params)
        h_proj_scale.grid(row=row, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        h_proj_entry = ttk.Entry(params_frame, textvariable=self.h_proj_var, width=10)
        h_proj_entry.grid(row=row, column=2, padx=5, pady=2)
        row += 1
        ttk.Label(params_frame, text="偏移量（单位：百分比）").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        row+=1
        # offset_hor
        ttk.Label(params_frame, text="水平方向偏移量(向左为正):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.offset_hor_var = tk.DoubleVar(value=self.params['offset_hor'])
        offset_hor_scale = ttk.Scale(params_frame, from_=-2.0, to=2.0, variable=self.offset_hor_var, orient='horizontal', command=self.update_params)
        offset_hor_scale.grid(row=row, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        offset_hor_entry = ttk.Entry(params_frame, textvariable=self.offset_hor_var, width=10)
        offset_hor_entry.grid(row=row, column=2, padx=5, pady=2)
        row += 1
        
        # offset_ver
        ttk.Label(params_frame, text="垂直方向偏移量(向上为正):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.offset_ver_var = tk.DoubleVar(value=self.params['offset_ver'])
        offset_ver_scale = ttk.Scale(params_frame, from_=-2.0, to=2.0, variable=self.offset_ver_var, orient='horizontal', command=self.update_params)
        offset_ver_scale.grid(row=row, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        offset_ver_entry = ttk.Entry(params_frame, textvariable=self.offset_ver_var, width=10)
        offset_ver_entry.grid(row=row, column=2, padx=5, pady=2)
        row += 1
        
        # scale
        ttk.Label(params_frame, text="缩放倍数:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.scale_var = tk.DoubleVar(value=self.params['scale'])
        scale_scale = ttk.Scale(params_frame, from_=0.1, to=5.0, variable=self.scale_var, orient='horizontal', command=self.update_params)
        scale_scale.grid(row=row, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        scale_entry = ttk.Entry(params_frame, textvariable=self.scale_var, width=10)
        scale_entry.grid(row=row, column=2, padx=5, pady=2)
        row += 1
        
        ttk.Label(params_frame, text="坐标轴的旋转角度(单位：度):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        row+=1
        # alpha
        ttk.Label(params_frame, text="绕x轴旋转角度:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.alpha_var = tk.DoubleVar(value=self.params['alpha'])
        alpha_scale = ttk.Scale(params_frame, from_=-180.0, to=180.0, variable=self.alpha_var, orient='horizontal', command=self.update_params)
        alpha_scale.grid(row=row, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        alpha_entry = ttk.Entry(params_frame, textvariable=self.alpha_var, width=10)
        alpha_entry.grid(row=row, column=2, padx=5, pady=2)
        row += 1
        
        # beta
        ttk.Label(params_frame, text="绕y轴旋转角度:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.beta_var = tk.DoubleVar(value=self.params['beta'])
        beta_scale = ttk.Scale(params_frame, from_=-180.0, to=180.0, variable=self.beta_var, orient='horizontal', command=self.update_params)
        beta_scale.grid(row=row, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        beta_entry = ttk.Entry(params_frame, textvariable=self.beta_var, width=10)
        beta_entry.grid(row=row, column=2, padx=5, pady=2)
        row += 1
        
        # gamma
        ttk.Label(params_frame, text="绕z轴旋转角度:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.gamma_var = tk.DoubleVar(value=self.params['gamma'])
        gamma_scale = ttk.Scale(params_frame, from_=-180.0, to=180.0, variable=self.gamma_var, orient='horizontal', command=self.update_params)
        gamma_scale.grid(row=row, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        gamma_entry = ttk.Entry(params_frame, textvariable=self.gamma_var, width=10)
        gamma_entry.grid(row=row, column=2, padx=5, pady=2)
        row += 1
        
        ttk.Label(params_frame, text="拉伸图片(高与宽的比例):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.skq_var = tk.DoubleVar(value=self.skq)
        skq_scale = ttk.Scale(params_frame, from_=0.1, to=10, variable=self.skq_var, orient='horizontal', command=self.update_params)
        skq_scale.grid(row=row, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        skq_entry = ttk.Entry(params_frame, textvariable=self.skq_var, width=10)
        skq_entry.grid(row=row, column=2, padx=5, pady=2)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="生成并保存", command=self.process_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="预览", command=self.preview_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="重置参数", command=self.reset_params).pack(side=tk.LEFT, padx=5)
        
        # Preview display in right panel
        preview_label_frame = ttk.Frame(right_frame)
        preview_label_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), pady=5)
        ttk.Label(preview_label_frame, text="图像生成较慢，结果不含白色部分").pack(side=tk.LEFT)
        
        # Canvas for preview with scrollbars
        self.canvas_frame = ttk.Frame(right_frame)
        self.canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.canvas = tk.Canvas(self.canvas_frame, bg='white', width=400, height=300)
        v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Store preview image reference
        self.preview_image_id = None
        self.preview_photo = None
        
        # Configure grid weights
        params_frame.columnconfigure(1, weight=1)
        
    def browse_img(self):
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif")]
        )
        if file_path:
            self.path_img = file_path
            self.img_path_var.set(file_path)
    
    def browse_proj(self):
        file_path = filedialog.asksaveasfilename(
            title="Select Projection Output Path",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            self.path_proj = file_path
            self.proj_path_var.set(file_path)
    
    def update_params(self, value):
        # This is called when any slider is moved
        # The variables are automatically updated, so no additional action needed
        pass
    
    def reset_params(self):
        self.w_proj_var.set(800)
        self.h_proj_var.set(600)
        self.offset_hor_var.set(0.0)
        self.offset_ver_var.set(0.0)
        self.scale_var.set(1.2)
        self.alpha_var.set(0.0)
        self.beta_var.set(0.0)
        self.gamma_var.set(0.0)
        self.skq_var.set(1.0)
    
    def preview_image(self):
        # Validate image path
        if not self.path_img:
            messagebox.showerror("Error", "Please select an image path first")
            return
            
        # Get current parameter values
        try:
            params = {
                'w_proj': self.w_proj_var.get(),
                'h_proj': self.h_proj_var.get(),
                'offset_hor': self.offset_hor_var.get(),
                'offset_ver': self.offset_ver_var.get(),
                'scale': self.scale_var.get(),
                'alpha': self.alpha_var.get(),
                'beta': self.beta_var.get(),
                'gamma': self.gamma_var.get()
            }
        except tk.TclError:
            messagebox.showerror("Error", "Invalid parameter value detected")
            return
        
        # Call the getimage function with current parameters (using temp path for preview)
        try:
            # Use a temporary path for preview
            result_img :Image.Image= getimage(self.path_img, "/tmp/preview.png", **params)
            # Resize image to fit display area (max 400x300 for preview)
            p = self.skq_var.get()
            result_img = result_img.resize((int(result_img.height*p),result_img.width))
            
            img_width, img_height = result_img.size
            max_width, max_height =  600,450
            
            # Calculate scaling factor to fit within max dimensions while maintaining aspect ratio
            scale_factor = min(max_width / img_width, max_height / img_height, 1.0)
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            
            # Resize the image
            resized_img = result_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for display
            self.preview_photo = ImageTk.PhotoImage(resized_img)
            
            # Clear the canvas and add the new image
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_photo)
            
            # Update scroll region
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating preview:\n{str(e)}")
    
    def process_image(self):
        self.path_proj = self.proj_path_var.get()
        # Validate file paths
        if not self.path_img or not self.path_proj:
            messagebox.showerror("Error", "Please select both image path and projection path")
            return
            
        # Get current parameter values
        try:
            params = {
                'w_proj': self.w_proj_var.get(),
                'h_proj': self.h_proj_var.get(),
                'offset_hor': self.offset_hor_var.get(),
                'offset_ver': self.offset_ver_var.get(),
                'scale': self.scale_var.get(),
                'alpha': self.alpha_var.get(),
                'beta': self.beta_var.get(),
                'gamma': self.gamma_var.get()
            }
        except tk.TclError:
            messagebox.showerror("Error", "Invalid parameter value detected")
            return
        
        # Call the getimage function with current parameters
        try:
            result_img:Image.Image = getimage(self.path_img, self.path_proj, **params)
            p = self.skq_var.get()
            result_img = result_img.resize((int(result_img.height*p),result_img.width))
            result_img.save(self.path_proj)
            # Show success message
            messagebox.showinfo("Success", f"Image processed and saved to:\n{self.path_proj}")
            
        except Exception as e:
            raise
            messagebox.showerror("Error", f"An error occurred while processing the image:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingGUI(root)
    root.mainloop()



