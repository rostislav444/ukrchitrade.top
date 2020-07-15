from django.db import models
from project import settings
import PIL
from PIL import Image, ImageOps
from django.utils.text import slugify
import unidecode
import os
import shutil 
from preview_generator.manager import PreviewManager





def imageFilename(self, filename):
    ext = filename.split('.')[-1]
    app_name = self._meta.app_label
    model_name = self._meta.model_name

    name_attrs = ['id'+str(self.pk)]
    name = ''
    parent = self
    models_attrs = ['slug','code']
    while parent != None:
        for attr in models_attrs:
            if hasattr(parent, attr):
                if getattr(parent, attr) != None:
                    name_attrs.insert(0, str(getattr(parent, attr)))
        if hasattr(parent, 'brand'):
            name_attrs.insert(0, str(parent.brand.slug))
        if hasattr(parent, 'parent'):
            parent = parent.parent
        else:
            parent = None
    name = '_'.join(name_attrs)
    name = slugify(str(name))
    

    # APP NAME PATH
    app_name_path = settings.MEDIA_ROOT + app_name + '/'
    app_name_dir =   os.path.isdir(app_name_path)
    if app_name_dir == False:
        os.mkdir(app_name_path)

    # MODEL NAME PATH
    model_name_path = settings.MEDIA_ROOT + app_name + '/' + model_name + '/'
    model_name_dir = os.path.isdir(model_name_path)
    if model_name_dir == False:
        os.mkdir(model_name_path)

    path =  '/'.join([app_name, model_name])
    
    return path, name, ext


class OneFile(models.Model):
    num =        models.PositiveIntegerField(default=0, blank=True, verbose_name="Номер") 
    name =       models.CharField(max_length=100, blank=True, default="", verbose_name="Название")
    slug =       models.CharField(max_length=250, blank=True, null=True, verbose_name="Иденитификатор", editable=False)
    file =       models.FileField(upload_to='temp', blank=False, null=True)
    file_url =   models.CharField(max_length=1000, blank=True, editable=False)
    ext =        models.CharField(max_length=100, blank=True, editable=False, verbose_name="file extension")

    class Meta:
        ordering = ['-num']
        abstract = True

    def save(self):
        print(self.file.name)
        super(OneFile, self).save()

        if len(self.name) == 0:
            try:
                modelName =  self.__class__._meta.verbose_name.title()
                self.name = ' '.join([modelName, self.product.category.name, self.product.name, self.product.code])
            except:
                self.name = self.__class__.__name__
      


        self.slug = slugify(unidecode.unidecode(self.name) + '-' + str(self.pk))
        if self.file.url != '/media/' + self.file_url:
            path, name, ext = imageFilename(self, self.file.name)
            self.ext = ext.lower()
            
            # f_name = 

            filename =  f'{path}/{self.slug}.{ext}'
            tempFile = self.file.name
            with open(settings.MEDIA_ROOT + self.file.name, "rb") as f1:
                raw = f1.read()
                with open(settings.MEDIA_ROOT + filename, 'wb') as f:
                    f.write(raw)

            setattr(getattr(self, 'file'), 'name', filename)
            setattr(self, 'file_url', filename)

            try: os.remove(settings.MEDIA_ROOT + tempFile)
            except: pass
            
        super(OneFile, self).save()


    def delete(self):
        try:
            os.remove(settings.MEDIA_ROOT + self.file.name)
        except: pass
        super(OneFile, self).delete()



class OneImage(models.Model):
    num =         models.PositiveIntegerField(default=0, blank=True, verbose_name="Номер") 
    image =       models.ImageField(blank=False, null=True)
    image_size  = models.CharField(max_length=1000, blank=True, editable=False)
    image_url   = models.CharField(max_length=1000, blank=True, editable=False)
  

    class Meta:
        ordering = ['-num']
        abstract = True


    def save(self):
        super(OneImage, self).save()
        if self.image.url != '/media/' + self.image_url:
            path, name, ext = imageFilename(self, self.image.name)
            img = Image.open(self.image._get_file())
            if ext.lower() == 'png':
                bg = Image.new("RGBA", img.size, "WHITE") 
                bg.putalpha(255)

                try:
                    bg.paste(img, (0, 0), img)      
                except:
                    bg.paste(img, (0, 0))      
                img = bg.convert('RGB')
                ext = 'JPEG'

            temp_img_path = settings.MEDIA_ROOT + 'temp-image.' + ext
            img.save(temp_img_path, quality=100)
            img.close()
            

            # CREATE IMAGES
          
            img = Image.open(temp_img_path)
            filename =  f'{path}/{name}.{ext}'
            setattr(getattr(self, 'image'), 'name', filename)

            img.thumbnail((1080, 1080), Image.ANTIALIAS)
                
            setattr(self, 'image_size', str(img.size[0]) + 'x' + str(img.size[1]))
            setattr(self, 'image_url', filename)
            img.save(settings.MEDIA_ROOT +  filename, quality=100)
            img.close()

            # Remove temp file
            try: os.remove(temp_img_path)
            except: pass

            fields = self._meta.get_fields()
        super(OneImage, self).save()



    def delete(self):
        path = getattr(self, 'image_url')
        try:
            os.remove(settings.MEDIA_ROOT + self.image.name)
        except: pass
        super(OneImage, self).delete()


# IMAGES
class Images(models.Model):
    num = models.PositiveIntegerField(default=0, blank=True, verbose_name="Номер") 
    # LARGE
    image_l =       models.ImageField(max_length=1000, blank=False, null=True, editable=True)
    image_l_size =  models.CharField(max_length=1000, blank=True, editable=False)
    image_l_url =   models.CharField(max_length=1000, blank=True, editable=False)
    # # MEDIUM
    # image_m =       models.ImageField(blank=True, null=True, editable=False)
    # image_m_size  = models.CharField(max_length=1000, blank=True, editable=False)
    # image_m_url   = models.CharField(max_length=1000, blank=True, editable=False)
    # SMALL
    image_s       = models.ImageField(blank=True, null=True, editable=False)
    image_s_size  = models.CharField(max_length=1000, blank=True, editable=False)
    image_s_url   = models.CharField(max_length=1000, blank=True, editable=False)
    # EXTRA SMALL
    image_xs      = models.ImageField(blank=True, null=True, editable=False)
    image_xs_size = models.CharField(max_length=1000, blank=True, editable=False)
    image_xs_url  = models.CharField(max_length=1000, blank=True, editable=False)
    # SQUARE 1200px * 1200px
    image_sq      = models.ImageField(blank=True, null=True, editable=True)
    image_sq_size = models.CharField(max_length=1000, blank=True, editable=False)
    image_sq_url  = models.CharField(max_length=1000, blank=True, editable=False)
    # REGENERATE
    regen = models.BooleanField(default=False, editable=True)
    ext =   models.CharField(max_length=100, default='jpeg', blank=True, editable=False, verbose_name="file extension")


    class Meta:
        ordering = ['-num']
        abstract = True


    def save(self):
        super(Images, self).save()
        if self.image_l.url != '/media/' + self.image_l_url or self.regen == True:
            img_path = settings.MEDIA_ROOT  + self.image_l.name
         
            img = None
            for size in ['l', 'sq']:
                try:
                    img = getattr(self, 'image_' + size)
                    img._get_file()
                    break
                except: continue

            if img is not None:
                path, name, ext = imageFilename(self, img.name)
                img = Image.open(img._get_file())
                if ext.lower() == 'png':
                    bg = Image.new("RGBA", img.size, "WHITE") 
                    img.putalpha(255)
                    bg.paste(img, (0, 0), img)              
                    img = bg.convert('RGB')
                    ext = 'JPEG'

                temp_img_path = settings.MEDIA_ROOT + path + 'temp-image.' + ext
                img.save(temp_img_path, quality=100)
                img.close()
            else: raise FileNotFoundError

            try: os.remove(self.image_l.url)
            except: pass
            
        
            sizes = (
                ('xs', 160),
                ('s',  480),
                ('l',  1200),
                ('sq', 1200),
            )

            def make_square(image, min_size=1200):  
                x, y = img.size
                z = x / y
                if z > 1:
                    x = 1200
                    y = int(x / z)
                else:
                    x = int(1200 * z)
                    y = 1200
                image = image.resize((x, y), resample=Image.LANCZOS)
            
                size = (1200, 1200)
                if ext == 'png':
                    background = Image.new("RGBA", size, (0,0,0,0))
                else:
                    background = Image.new("RGB", size, "WHITE")
                    
                background.paste(
                    image, (int((size[0] - image.size[0]) / 2), int((size[1] - image.size[1]) / 2))
                )
                return background

            # CREATE IMAGES
            for key, res in sizes:
                img = Image.open(temp_img_path)
                filename =  f'{path}/{name}_{key}.{ext}'
                setattr(getattr(self, 'image_' + key ), 'name', filename)
                
                if key == 'sq':
                    img = make_square(img, min_size=res)
                else:
                    img.thumbnail((res, res), Image.ANTIALIAS)
                   
                setattr(self, 'image_' + key + '_size', str(img.size[0]) + 'x' + str(img.size[1]))
                setattr(self, 'image_' + key + '_url', filename)
                img.save(settings.MEDIA_ROOT +  filename, quality=100)
                img.close()

            # Remove temp file
            try: os.remove(img_path)
            except: pass
            try: os.remove(temp_img_path)
            except: pass

            fields = self._meta.get_fields()
            # for i in fields:
            #     print(i.get_internal_type())
        self.regen = False
        super(Images, self).save()



    def delete(self):
        for key in ['l','s','xs','sq']:
            path = getattr(self, 'image_' + key + '_url')
            try:
                os.remove(settings.MEDIA_ROOT + path)
            except: pass
        super(Images, self).delete()








