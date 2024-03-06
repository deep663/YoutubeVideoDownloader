from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
                            QListWidget, QListWidgetItem, QFileDialog, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from youtubesearchpython import VideosSearch
from pytube import YouTube

class PodcastDownloader(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Youtube Video Downloader')
        self.setGeometry(100, 100, 600, 400)

        # Add a logo
        logo_label = QLabel(self)
        pixmap = QPixmap('download.png')
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        self.labelQuery = QLabel('Enter search query:')
        self.queryLineEdit = QLineEdit(self)
        self.btnSearch = QPushButton('Search', self)
        self.btnSearch.clicked.connect(self.searchAndDisplay)

        self.resultList = QListWidget()

        self.btnDownloadSelected = QPushButton('Download Selected', self)
        self.btnDownloadSelected.clicked.connect(self.downloadSelected)

        self.btnSelectFolder = QPushButton('Select Download Folder', self)
        self.btnSelectFolder.clicked.connect(self.selectDownloadFolder)

        self.downloadFolder = ''

        # Added ComboBox for choosing video or audio
        self.comboFormat = QComboBox(self)
        self.comboFormat.addItem('Video')
        self.comboFormat.addItem('Audio')

        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addWidget(self.labelQuery)
        layout.addWidget(self.queryLineEdit)
        layout.addWidget(self.btnSearch)
        layout.addWidget(self.resultList)
        layout.addWidget(self.btnDownloadSelected)
        layout.addWidget(self.btnSelectFolder)
        layout.addWidget(self.comboFormat)

        self.setLayout(layout)

    def searchAndDisplay(self):
        self.resultList.clear()
        query = self.queryLineEdit.text()

        videos_search = VideosSearch(query)
        results = videos_search.result()

        for idx, video in enumerate(results['result'], start=1):
            title = video['title']
            channel = video['channel']['name']
            link = video['link']
            item = QListWidgetItem(f"{idx}. {title} by {channel}")
            item.setData(100, link)  # Store the link as data
            self.resultList.addItem(item)

    def downloadSelected(self):
        if not self.downloadFolder:
            self.selectDownloadFolder()

        selected_items = self.resultList.selectedItems()
        if not selected_items:
            return

        download_videos = True
        format_choice = self.comboFormat.currentText()

        for item in selected_items:
            link = item.data(100)
            try:
                yt = YouTube(link)
                if format_choice == 'Video':
                    stream = yt.streams.get_highest_resolution()
                else:  # Audio
                    stream = yt.streams.filter(only_audio=True).first()
                title = yt.title
                print(f"Downloading {title} to {self.downloadFolder}...")
                stream.download(output_path=self.downloadFolder)
                print(f"Download of {title} complete.")
            except Exception as e:
                print(f"Error downloading {title}: {e}")

    def selectDownloadFolder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Download Folder')
        if folder:
            self.downloadFolder = folder
            print(f"Download folder set to: {folder}")

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = PodcastDownloader()
    window.show()
    sys.exit(app.exec_())
