import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyperclip
import threading
from deep_translator import GoogleTranslator

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeAlpha AI Translator Pro")
        self.root.geometry("600x650")
        
        # Mapping for dropdown menu
        self.langs = {"English": "en", "Spanish": "es", "French": "fr", "German": "de", "Italian": "it"}
        
        # UI Components
        tk.Label(root, text="🌍 AI Translation Tool", font=("Arial", 16, "bold")).pack(pady=10)
        
        tk.Label(root, text="Enter Text:").pack()
        self.text_input = tk.Text(root, height=6, width=60)
        self.text_input.pack(pady=5)
        
        tk.Label(root, text="Select Target Language:").pack()
        self.lang_dropdown = ttk.Combobox(root, values=list(self.langs.keys()), state="readonly")
        self.lang_dropdown.set("Spanish")
        self.lang_dropdown.pack(pady=5)
        
        # Feedback and Progress
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='indeterminate')
        self.progress.pack(pady=5)
        
        # Button Grid
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Translate", command=self.start_translation_thread, bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Copy", command=self.copy, bg="#2196F3", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save", command=self.save_history, bg="#9C27B0", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear, bg="#FF9800", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        
        tk.Label(root, text="Result:").pack()
        self.text_output = tk.Text(root, height=6, width=60, state=tk.DISABLED)
        self.text_output.pack(pady=5)

    def start_translation_thread(self):
        """Starts translation in a background thread to prevent GUI freezing."""
        self.progress.start()
        threading.Thread(target=self.translate, daemon=True).start()

    def translate(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            self.progress.stop()
            messagebox.showwarning("Input Error", "Please enter text to translate!")
            return
        
        try:
            # Auto-detection is handled by 'auto' source
            target = self.langs[self.lang_dropdown.get()]
            translated = GoogleTranslator(source='auto', target=target).translate(text)
            
            self.text_output.config(state=tk.NORMAL)
            self.text_output.delete("1.0", tk.END)
            self.text_output.insert(tk.END, translated)
            self.text_output.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Network Error", f"Could not connect: {e}")
        finally:
            self.progress.stop()

    def copy(self):
        content = self.text_output.get("1.0", tk.END).strip()
        if content:
            pyperclip.copy(content)
            messagebox.showinfo("Clipboard", "Translation copied!")
        else:
            messagebox.showwarning("Warning", "Nothing to copy.")

    def save_history(self):
        content = self.text_output.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Empty", "No translation to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Saved", "Translation saved successfully!")

    def clear(self):
        self.text_input.delete("1.0", tk.END)
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete("1.0", tk.END)
        self.text_output.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()