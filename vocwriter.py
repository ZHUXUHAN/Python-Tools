from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom
from lxml import etree
import os
import sys
class PascalVocWriter:

    def __init__(
            self,
            foldername,#文件夹
            filename,#文件名
            imgSize,
            databaseSrc='Unknown',
            localImgPath=None,
            shape_type=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.shape_type = shape_type

    def prettify(self, elem):#修饰
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf8')#生成一个字符串来表示xml的element
        # rough_string = ElementTree.tostring(elem)#从字符串中生成xml树
        root = etree.fromstring(rough_string)#lxml下的fromstring
        return etree.tostring(root,pretty_print=True)

    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        '''
        if self.filename is None or \
                        self.foldername is None or \
                        self.imgSize is None or \
                        len(self.boxlist) <= 0:
        '''
        if self.filename is None or \
                len(self.boxlist) <= 0:
            return None

        top = Element('annotation')
        folder = SubElement(top, 'folder')
        folder.text = self.foldername

        filename = SubElement(top, 'filename')
        filename.text = self.filename

        localImgPath = SubElement(top, 'path')
        self.localImgPath = self.localImgPath.split('/')[-1]
        localImgPath.text = self.localImgPath

        source = SubElement(top, 'source')
        database = SubElement(source, 'database')
        database.text = self.databaseSrc

        if self.imgSize:
            size_part = SubElement(top, 'size')
            width = SubElement(size_part, 'width')
            height = SubElement(size_part, 'height')
            depth = SubElement(size_part, 'depth')
            width.text = str(self.imgSize[1])
            height.text = str(self.imgSize[0])
            if len(self.imgSize) == 3:
                depth.text = str(self.imgSize[2])
            else:
                depth.text = '1'

        segmented = SubElement(top, 'segmented')
        segmented.text = '0'
        shape_type = SubElement(top, 'shape_type')
        shape_type.text = self.shape_type
        return top

    def addBndBox(self, xmin, ymin, xmax, ymax, name):
        bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        bndbox['name'] = name
        self.boxlist.append(bndbox)

    def addPolygon(self, shape, name,instance_id):
        polygon = {}
        i = 0
        for point in shape:
            polygon[i] = point
            i = i + 1
        polygon['name'] = name
        polygon['point_num'] = str(len(shape))
        polygon['instance_id'] = instance_id
        self.boxlist.append(polygon)

    def appendObjects(self, top):
        for each_object in self.boxlist:
            object_item = SubElement(top, 'object')
            if each_object['name']:
                name = SubElement(object_item, 'name')
                name.text = str(each_object['name'])
            pose = SubElement(object_item, 'pose')
            pose.text = "Unspecified"
            if 'instance_id' in each_object.keys():
                instance_id = SubElement(object_item,'instance_id')
                instance_id.text = str(each_object['instance_id'])
            truncated = SubElement(object_item, 'truncated')
            truncated.text = "0"
            difficult = SubElement(object_item, 'difficult')
            difficult.text = "0"
            if self.shape_type == 'RECT':
                bndbox = SubElement(object_item, 'bndbox')
                xmin = SubElement(bndbox, 'xmin')
                xmin.text = str(each_object['xmin'])
                ymin = SubElement(bndbox, 'ymin')
                ymin.text = str(each_object['ymin'])
                xmax = SubElement(bndbox, 'xmax')
                xmax.text = str(each_object['xmax'])
                ymax = SubElement(bndbox, 'ymax')
                ymax.text = str(each_object['ymax'])
            elif self.shape_type == 'POLYGON':
                polygon = SubElement(object_item, 'polygon')
                for i in range(int(each_object['point_num'])):
                    point = SubElement(polygon, 'point' + str(i))
                    point.text = str(
                        int(each_object[i][0])) + ',' + str(int(each_object[i][1]))
                    print (i, point.text)

    def save(self, targetFile=None):
        root = self.genXML()
        self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = open(self.filename + '.xml', 'w')
        else:
            print('save xml path:',targetFile)
            print('correct path：',targetFile.split('/'+self.filename+'.xml')[0])
            try:
                out_file = open(str(targetFile), 'w')
            except FileNotFoundError:
                print('error tackle:',targetFile.split('/'+self.filename+'.xml')[0])
                if not os.path.exists(targetFile.split(self.filename+'.xml')[0]):
                    os.makedirs(targetFile.split('/'+self.filename+'.xml')[0])#创建文件夹的层级路径
                out_file = open(str(targetFile), 'w')

        out_file.write(str(self.prettify(root).decode()))
        out_file.close()
class LabelFile(object):
    # It might be changed as window creates
    suffix = '.lif'

    def __init__(self, filename=None):
        self.shapes = ()
        self.imagePath = None
        self.imageData = None
        if filename is not None:
            self.load(filename)

    def savePascalVocFormat(
            self,
            savefilename,
            image_size,
            shapes,
            imagePath=None,
            databaseSrc=None,
            shape_type_='RECT'):
        print(imagePath)
        imgFolderPath = os.path.dirname(imagePath)#返回文件路径的目录
        imgFolderName = os.path.split(imgFolderPath)[-1]#
        imgFileName = os.path.basename(imagePath)#获得文件名，包括后缀
        imgFileNameWithoutExt = os.path.splitext(imgFileName)[0]#获取文件名（包括后缀）文件名
        print('imgaeFolderPath:',imgFolderPath)
        print('imgaeFolderName:', imgFolderName)
        print('imgFileName:',imgFileName)
        print(' imgFileNameWithoutExt:',imgFileNameWithoutExt)


        #img = cv2.imread(imagePath)
        writer = PascalVocWriter(
            imgFolderName,
            imgFileNameWithoutExt,
            image_size,
            localImgPath=imagePath,
            shape_type=shape_type_)
        bSave = False
        for shape in shapes:
            label = shape['label']
            if shape['shape_type'] == 0:
                print ('add rects')#添加框子

                bndbox=shape['points']
                writer.addBndBox(
                    bndbox[0],
                    bndbox[1],
                    bndbox[2],
                    bndbox[3],
                    label)
            if shape['shape_type'] == 1:
                print ('add polygons')#添加分割点
                writer.addPolygon(points, label,instance_id=shape['instance_id'])


            bSave = True
            print('label savefilename:',savefilename)

        if bSave:
            writer.save(targetFile=savefilename)#这里存储
        return

    @staticmethod
    def isLabelFile(filename):
        fileSuffix = os.path.splitext(filename)[1].lower()
        return fileSuffix == LabelFile.suffix


# lf=LabelFile()
# xmlname='/home/priv-lab1/workspace/zxh/pet-project/test.xml'
# imgname='/home/priv-lab1/workspace/zxh/pet-project/test.jpg'
# shapes=[{'points':[1,1,1,1],'label':'a','shape_type':0}]
# lf.savePascalVocFormat(xmlname,image_size=[20,20],shapes=shapes,imagePath=imgname)
