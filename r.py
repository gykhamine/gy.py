import os

def nt():
	l=[
	#plymouth
	'os.system("sudo plymouth-set-default-theme -R text")',
	'os.system("sudo grub2-mkconfig -o /boot/grub2/grub.cfg")',
	
	
# netoyer	
	'os.system("sudo rm -rf /usr/share/backgrounds ")',
	'os.system("sudo rm -rf /usr/share/plymouth/themes/details ")',
	'os.system("sudo rm -rf /usr/share/plymouth/themes/charge")',
	'os.system("sudo rm -rf /usr/share/plymouth/themes/tribar") ',
	'os.system("sudo rm -rf /usr/share/plymouth/themes/bgrt")',
	'os.system("sudo rm -rf /usr/share/plymouth/themes/spiner")',
	'os.system("sudo rm -rf /afs")',
	'os.system("sudo rm -rf /home/gykhamine/.local/share/flatpak")',
	'os.system("sudo rm -rf /home/gykhamine/.local/share/gnome-boxes")',
	'os.system("sudo rm -rf /home/gykhamine/.local/share/applications ")',
	'os.system("sudo rm -rf /home/gykhamine/.local/share/gnome-backgrounds")',
	'os.system("sudo rm -rf /home/gykhamine/.local/share/gnome-software")',
	'os.system("sudo rm -rf /home/gykhamine/.local/share/gnome-icons")',
	'os.system("sudo rm -rf /lost+found")'
	'os.system("sudo rm -rf /usr/share/gnome-shell/extensions/{*,.*}")',
	'os.system("sudo rm -rf /usr/share/themes/Emacs")'
	'os.system("sudo rm -rf /usr/share/themes/HighContrast")',
	'os.system("sudo rm -rf /usr/share/themes/Default")',
	'os.system("sudo rm -rf /usr/share/themes/Raleigh")',
	'os.system("sudo rm -rf /usr/share/icons/AdwaitaLegacy")',
	'os.system("sudo rm -rf /usr/share/icons/breeze")',
	'os.system("sudo rm -rf /usr/share/icons/breeze-dark")',
	'os.system("sudo rm -rf /usr/share/icons/default")',
	'os.system("sudo rm -rf /usr/share/icons/hicolor)',
	'os.system("sudo rm -rf /usr/share/icons/HighContrast")',
	'os.system("sudo rm -rf /usr/share/icons/locolor")',
	'os.system("sudo rm -rf /usr/share/icons/oxygen")'
	'os.system("sudo rm  /usr/share/icons/gnome-logo-text-dark.svg")',
	'os.system("sudo rm  /usr/share/icons/gnome-logo-text.svg")',
	'os.system("sudo rm -rf /usr/share/polkit-1/rules.d/{*,.*}")'
	'os.system("sudo rm -rf /var/www/html")',
		
		
		
# supprimer les icons		
	' os.system("sudo rm  /usr/share/applications/org.gnome.tweaks.desktop")',
	'os.system("sudo rm  /usr/share/applications/org.gnome.Extensions.desktop")',
	'os.system("sudo rm  /usr/share/applications/org.gnome.Ptyxis.desktop")',
	'os.system("sudo rm  /usr/share/applications/org.gnome.TextEdito.desktop")',
	'os.system("sudo rm  /usr/share/applications/org.gnome.Nautilus.desktop")',
	'os.system("sudo rm  /usr/share/applications/org.gnome.Settings.desktop")',
	'os.system("sudo rm  /usr/share/applications/org.mozilla.firefox.desktop")',
	'os.system("sudo rm  /usr/share/applications/io.github.antimicrox.antimicrox.desktop")',
	'os.system("sudo rm  /usr/share/applications/torbrowser.desktop")',
	'os.system("sudo rm  /usr/share/applications/torbrowser-settings.desktop")',
		
		
		
		
		
		
# disperser les element gy		
		
	'os.system("sudo mv /Gykhamine/scripts/conf/gykhamine.rules /usr/share/polkit-1/rules.d/gykhamine.rules")',
	'os.system("sudo mv /Gykhamine/scripts/conf/gykhamine.conf /etc/nginx/confd/gykhamine2.conf")',
	'os.system("sudo mv /Gykhamine/scripts/conf/gykhamine2.conf /etc/nginx/confd/gykhamine2.conf")',
	'os.system("sudo mv /Gykhamine/scripts/conf/Gykhamine.desktop /usr/share/applications/Gykhamine.desktop ")',
	'os.system("sudo mv -r /Gykhamine/scripts/conf/mycerts /mycertsec/ssl/mycerts")',
	'os.system("sudo mv -r /Gykhamine/scripts/conf/html /var/www/html")',	
	'os.system("sudo rm -rf /home/gykhamine/Videos")',
		
		
		
		
	
		
	
		
# configure le serveur		
	'os.system("sudo firewall-cmd --permanent --add-service=https")',
	'os.system(sudo firewall-cmd --reload")',
	"os.system('sudo systemctl enable nginx')",
	"os.system('sudo systemctl enable php-fpm')"
	]
	x=len(l)
	i=0
	while i<x:
	        c=l[i]
	        try :
	        	#os.system(c)
	        	print(c)
	        except Exception as e:
	        	print(e)
	        i=i+1
	        
def inst():	     
	w=[' generic-logos ' ,'nginx','pip','openssl',"antimicrox","php","python-tkinter","python-pyaudio","g++","livecd-tools","nmap","john","netcat","gnucobol","aircrack-ng","python-beatifulsoup4","python-humanize","python-lxml","python-soupsieve","gnome-shell-extensions-blur-my-shell","gnome-shell-extensions-dash-to-panel","fastfech","gnome-tweaks","gnome-extensions-app"]
	x=len(w)
	i=0
	while i<x:	
  	   c = " sudo dnf -y install "+ w[i]
  	   c1 = "sudo dnf install" +w[i]+"--allowerading"
  	   if i==0: 
  	     # os.system(c1)
  	     print (c1)
  	   else:
  	   	 # os.system(c)
  	   	 print (c)
  	   i=i+1
  	   	 
def pip():
  	    v=["opencv-python","numpy","scipy","matplotlib","kivi cython buildozer","crypto","pyinstaller pydub moviepy","esptool","django gunicorn","panda","scrapy", "beautifulsoup4", "selenium", "requests", "playwright", "pyquery", "lxml","PyPDF2", "pdfminer", "pdfquery", "pdfplumber", "reportlab","geopy", "folium", "gmplot", "geopandas", "osmapi","stem", "pycurl", "requests-tor","paramiko", "fabric", "pysftp","customtkinter","qrcode","pyaudio","pocketsphinx","SpeechRecognition","keras","scikit-learn"]
  	    x=len(v)
  	    i=0
  	    while i<x:
  	    	 c = "pip install "+ v[i]
  	    	 os.system(c)
  	    	 print (c)
  	    	 i=i+1
  	    	 
  	    	
   

def rm():
    t=["httpd","flatpak","gnome-boxes", "gnome-contacts","gnome-calculator","gnome-clocks","Rhythmbox","gnome-maps","gnome-tour","yelp","gnome-weather","gnome-calandar", "gnome-connections","gnome-font-viewer","gnome-characters","totem","libreoffice-writer","libreoffice-calc","libreoffice-impress","gnome-maps","snapshot","simple-scan","gnome-logs","loupe","gnome-system-monitor","mediawriter","gnome-disk-utility","gnome-abrt","evince","baobab"]
    x=len(t)
    i=0
    while i<x:
    	c = " sudo dnf -y remove "+ t[i]
    	# os.system(c)
    	print (c)
    	i=i+1
pass    
    
    


  	  
  	    
    	 
       	 
       	 
    	 
       	 
       	 
    	    	        
	        
	       
    
#os.system("sudo mv -r /home/gykhamine/gykhaminemv /gykhamine ")
# os.system("gsettings set org.gnome.desktop.background picture-uri 'file:///gykhamine/3.png'")




   
pip() 

    
    

    
    
    
    
    
    
    




    
    
    
     
    

    
        
            
                

                        
                                                
                                                                   

                                                                 
                                                                                                             
                                                                                                                                                         
                                                                                                                                                                                                                                                 

