import json
import sys
import os
import requests
import re
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt

class MovieApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("movieScraping.ui", self)

        # Inisialisasi list data
        self.movies = []
        self.movies_top10 = []

        # =========================
        # STYLE & UI SETUP
        # =========================
        self.apply_style()
        self.menu_buttons = [self.pushButton_3, self.pushButton_4, self.pushButton_5, self.pushButton_6]
        for btn in self.menu_buttons:
            btn.setObjectName("menu")

        # Navigation
        self.pushButton_3.clicked.connect(lambda: self.switch_page(0))
        self.pushButton_4.clicked.connect(lambda: self.switch_page(1))
        self.pushButton_5.clicked.connect(lambda: self.switch_page(2))
        self.pushButton_6.clicked.connect(lambda: self.switch_page(3))

        # Table Config
        headers = ["Title", "Year", "Rating", "Genre", "Duration", "Platform"]
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.cellClicked.connect(self.show_movie_detail_top10)

        self.tableWidget_2.setColumnCount(6)
        self.tableWidget_2.setHorizontalHeaderLabels(headers)
        self.tableWidget_2.cellClicked.connect(self.show_movie_detail)

        # Button Scrape
        self.pushButton_2.clicked.connect(self.scrape_data)

        # Default Page & Initial Load
        self.switch_page(0)
        self.load_from_json() # Ini akan otomatis ngisi tableWidget dan tableWidget_2
        self.update_dashboard()

    def apply_style(self):
        self.setStyleSheet("""
            QWidget { background-color: #f5f6fa; font-family: Segoe UI; }
            QPushButton { background-color: white; border-radius: 8px; padding: 6px; }
            QPushButton:hover { background-color: #dfe6e9; }
            QPushButton#active { background-color: #0984e3; color: white; font-weight: bold; }
            QTableWidget { background-color: white; border-radius: 10px; gridline-color: #f0f0f0; }
            QHeaderView::section { background-color: #0984e3; color: white; padding: 5px; border: none; }
        """)

    def switch_page(self, index):
        self.stackedWidget.setCurrentIndex(index)
        for i, btn in enumerate(self.menu_buttons):
            btn.setObjectName("active" if i == index else "menu")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # =========================
    # DATA LOADING & RENDERING
    # =========================
    def load_from_json(self):
        file_target = "data_film.json"
        if os.path.exists(file_target):
            try:
                with open(file_target, "r", encoding="utf-8") as f:
                    data_raw = json.load(f)
                
                self.movies = []
                for item in data_raw:
                    # Gabungkan data jadi list agar indexnya konsisten [0..6]
                    movie = [
                        item.get("title", "N/A"),
                        item.get("year", "N/A"),
                        item.get("rating", "N/A"),
                        item.get("genre", "Unknown"),
                        item.get("duration", "N/A"),
                        item.get("link", "N/A"), # Ini URL Platform Icon
                        item.get("poster", "")
                    ]
                    self.movies.append(movie)
                
                self.movies_top10 = self.movies[:10]
                
                # Render ke kedua tabel
                self._render_universal(self.tableWidget, self.movies_top10) # Tabel Top 10
                self._render_universal(self.tableWidget_2, self.movies)     # Tabel Database
                self.update_dashboard()
                print(f"✅ Data loaded: {len(self.movies)} movies.")
            except Exception as e:
                print(f"⚠️ Load Error: {e}")

    def _render_universal(self, table_widget, data_list):
        table_widget.setRowCount(0)
        if not data_list: return

        for movie in data_list:
            row = table_widget.rowCount()
            table_widget.insertRow(row)

            for col in range(6):
                val = str(movie[col])
                
                # Kolom Platform (Index 5) -> Tampilkan Icon
                if col == 5 and val.startswith("http"):
                    try:
                        fixed_url = val.replace(".avif", ".png").replace(".webp", ".png")
                        resp = requests.get(fixed_url, timeout=3)
                        pixmap = QPixmap()
                        if pixmap.loadFromData(resp.content):
                            item = QTableWidgetItem()
                            item.setIcon(QIcon(pixmap))
                            table_widget.setIconSize(QSize(35, 35))
                            table_widget.setItem(row, col, item)
                        else:
                            table_widget.setItem(row, col, QTableWidgetItem("Icon"))
                    except:
                        table_widget.setItem(row, col, QTableWidgetItem("N/A"))
                else:
                    # Kolom Teks Biasa
                    table_widget.setItem(row, col, QTableWidgetItem(val))
            
            table_widget.setRowHeight(row, 50)

    # =========================
    # MOVIE DETAILS
    # =========================
    def show_movie_detail_top10(self, row):
        if row < len(self.movies_top10):
            self.show_detail(self.movies_top10[row])

    def show_movie_detail(self, row):
        if row < len(self.movies):
            self.show_detail(self.movies[row])

    def show_detail(self, movie):
        # Set Teks
        self.label_17.setText(f"Title : {movie[0]}")
        self.label_18.setText(f"Year : {movie[1]}")
        self.label_19.setText(f"Rating : {movie[2]}")
        self.label_20.setText(f"Genre : {movie[3]}")
        self.label_21.setText(f"Duration : {movie[4]}")
        self.label_24.setText("Synopsis : N/A")

        # Platform Image (label_25)
        platform_url = movie[5]
        if platform_url.startswith("http"):
            try:
                fixed_url = platform_url.replace(".avif", ".png").replace(".webp", ".png")
                resp = requests.get(fixed_url, timeout=3)
                pix_p = QPixmap()
                if pix_p.loadFromData(resp.content):
                    self.label_25.setPixmap(pix_p.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.label_25.setText(platform_url)
            except:
                self.label_25.setText(platform_url)
        else:
            self.label_25.setText(platform_url)

        # Poster Image (label_5)
        if movie[6]:
            try:
                resp = requests.get(movie[6], headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
                pix_poster = QPixmap()
                pix_poster.loadFromData(resp.content)
                self.label_5.setScaledContents(True)
                self.label_5.setPixmap(pix_poster)
            except:
                self.label_5.setText("No Poster")

        self.stackedWidget.setCurrentWidget(self.page_7)
        self.pushButton_8.clicked.connect(lambda: self.switch_page(0))

    # =========================
    # SCRAPING LOGIC
    # =========================
    def scrape_data(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        wait = WebDriverWait(driver, 10)
        temp_data = []

        try:
            driver.get("https://www.imdb.com/chart/top/")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")))
            elements = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

            for item in elements[:15]: # Ambil 15 film
                try:
                    title = item.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text.split(". ", 1)[-1]
                    year = item.find_elements(By.CSS_SELECTOR, "span.cli-title-metadata-item")[0].text
                    duration = item.find_elements(By.CSS_SELECTOR, "span.cli-title-metadata-item")[1].text
                    rating = item.find_element(By.CSS_SELECTOR, "span.ipc-rating-star").text.split("\n")[0]
                    poster = item.find_element(By.TAG_NAME, "img").get_attribute("src")
                    
                    # Simpan data sementara
                    temp_data.append({
                        "title": title, "year": year, "rating": rating, 
                        "duration": duration, "poster": poster
                    })
                except: continue

            # Get Genre & Platform from JustWatch
            for film in temp_data:
                genre, platform = self.get_data_from_justwatch(driver, film['title'])
                film['genre'] = genre
                film['link'] = platform # Simpan URL icon ke key 'link'

            # Simpan ke file
            with open("data_film.json", "w", encoding="utf-8") as f:
                json.dump(temp_data, f, indent=4)
            
            print("💾 Scraping Selesai & Data Disimpan")
            
        finally:
            driver.quit()
            # Refresh Tampilan
            self.load_from_json() 
            self.switch_page(3) # Pindah ke Database Film

    def get_data_from_justwatch(self, driver, title):
        try:
            slug = re.sub(r'\s+', '-', re.sub(r'[^a-z0-9\s-]', '', title.lower())).strip('-')
            driver.get(f"https://www.justwatch.com/id/movie/{slug}")
            time.sleep(2)

            # Genre
            try:
                g = driver.find_element(By.XPATH, "//h3[contains(text(), 'Genre')]/following-sibling::div").text.replace("\n", ", ")
            except: g = "Unknown"

            # Platform Icon
            try:
                media = driver.find_elements(By.XPATH, "//*[@srcset or @src]")
                p = "Unknown"
                for el in media:
                    url = el.get_attribute("srcset") or el.get_attribute("src")
                    if url and "images.justwatch.com/icon" in url:
                        p = url.split(" ")[0]
                        break
            except: p = "Unknown"
            
            return g, p
        except: return "Unknown", "Unknown"

    def update_dashboard(self):
        if self.movies:
            self.label_4.setText(str(len(self.movies)))
            rates = []
            for m in self.movies:
                try: rates.append(float(m[2].split()[0]))
                except: pass
            avg = sum(rates)/len(rates) if rates else 0
            self.label_8.setText(f"{avg:.1f}")

            self.label_10.setText("N/A")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MovieApp()
    window.show()
    sys.exit(app.exec_())