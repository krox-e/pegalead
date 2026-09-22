import qrcode
import shutil

url = "https://pegalead-tau.vercel.app"
img = qrcode.make(url)
img.save("qrcode_vercel.png")

# Also save to artifact directory
dest = r"C:\Users\Pichau\.gemini\antigravity-ide\brain\6b13890f-0f41-4391-b0db-04a87d8cdb9f\qrcode_vercel.png"
shutil.copyfile("qrcode_vercel.png", dest)
print("QR Code salvo com sucesso em", dest)
