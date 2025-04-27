import sqlite3
import csv
import os
import datetime

class DatabaseManager:
    def __init__(self, db_name="smallbizz.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        # Enable foreign keys if needed for future relationships
        self.conn.execute("PRAGMA foreign_keys = ON")
        # Configure connection to return rows as dictionaries if necessary
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Check if the table exists
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
        table_exists = self.c.fetchone()
        
        if not table_exists:
            # Create new table with all columns if it doesn't exist
            self.c.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE,
                    name TEXT NOT NULL,
                    quantity INTEGER DEFAULT 0,
                    price REAL DEFAULT 0,
                    category TEXT,
                    notes TEXT,
                    created_at TEXT DEFAULT (datetime('now', 'localtime')),
                    updated_at TEXT DEFAULT (datetime('now', 'localtime'))
                )
            ''')
            self.conn.commit()
        else:
            # Check if notes column exists, if not, add it
            self.c.execute("PRAGMA table_info(items)")
            columns = [info[1] for info in self.c.fetchall()]
            
            if 'notes' not in columns:
                self.c.execute('ALTER TABLE items ADD COLUMN notes TEXT')
                self.conn.commit()
            
            if 'created_at' not in columns:
                # Add created_at column without default
                self.c.execute('ALTER TABLE items ADD COLUMN created_at TEXT')
                # Update all existing rows with current time
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.c.execute('UPDATE items SET created_at = ?', (current_time,))
                self.conn.commit()
            
            if 'updated_at' not in columns:
                # Add updated_at column without default
                self.c.execute('ALTER TABLE items ADD COLUMN updated_at TEXT')
                # Update all existing rows with current time
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.c.execute('UPDATE items SET updated_at = ?', (current_time,))
                self.conn.commit()
        
        # Create trigger to update timestamp
        self.c.execute("SELECT name FROM sqlite_master WHERE type='trigger' AND name='update_timestamp'")
        trigger_exists = self.c.fetchone()
        
        if not trigger_exists:
            self.c.execute('''
                CREATE TRIGGER update_timestamp 
                AFTER UPDATE ON items
                FOR EACH ROW
                BEGIN
                    UPDATE items SET updated_at = datetime('now', 'localtime') WHERE id = OLD.id;
                END
            ''')
            self.conn.commit()

    def insert_item(self, code, name, quantity, price, category, notes=""):
        """Insert a new item into the database"""
        try:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.c.execute('''
                INSERT INTO items (code, name, quantity, price, category, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (code, name, quantity, price, category, notes, current_time, current_time))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Handle duplicate code error
            self.conn.rollback()
            raise Exception(f"Kode barang '{code}' sudah ada dalam database")
        except Exception as e:
            self.conn.rollback()
            raise e

    def update_item(self, code, name, quantity, price, category, notes=""):
        """Update an existing item by code"""
        try:
            self.c.execute('''
                UPDATE items 
                SET name=?, quantity=?, price=?, category=?, notes=?
                WHERE code=?
            ''', (name, quantity, price, category, notes, code))
            
            if self.c.rowcount == 0:
                raise Exception(f"Item dengan kode '{code}' tidak ditemukan")
                
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise e

    def delete_item(self, code):
        """Delete an item by code"""
        try:
            self.c.execute('DELETE FROM items WHERE code=?', (code,))
            
            if self.c.rowcount == 0:
                raise Exception(f"Item dengan kode '{code}' tidak ditemukan")
                
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise e

    def fetch_all(self):
        """Fetch all items from the database"""
        self.c.execute('''
            SELECT code, name, quantity, price, category, notes
            FROM items
            ORDER BY name
        ''')
        return self.c.fetchall()

    def get_item_by_code(self, code):
        """Get a single item by its code"""
        self.c.execute('''
            SELECT code, name, quantity, price, category, notes
            FROM items
            WHERE code = ?
        ''', (code,))
        return self.c.fetchone()

    def search_items(self, keyword, filter_by):
        """Search items with various filters"""
        query = '''
            SELECT code, name, quantity, price, category, notes 
            FROM items
        '''
        params = ()

        if keyword:
            if filter_by == "Semua":
                query += " WHERE code LIKE ? OR name LIKE ? OR category LIKE ? OR notes LIKE ?"
                params = (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%')
            elif filter_by == "Kode":
                query += " WHERE code LIKE ?"
                params = (f'%{keyword}%',)
            elif filter_by == "Nama":
                query += " WHERE name LIKE ?"
                params = (f'%{keyword}%',)
            elif filter_by == "Kategori":
                query += " WHERE category LIKE ?"
                params = (f'%{keyword}%',)
            elif filter_by == "Catatan":
                query += " WHERE notes LIKE ?"
                params = (f'%{keyword}%',)

        query += " ORDER BY name"
        self.c.execute(query, params)
        return self.c.fetchall()

    def get_summary(self):
        """Get inventory summary statistics"""
        self.c.execute('''
            SELECT 
                COUNT(*) as total_items, 
                COALESCE(SUM(quantity), 0) as total_quantity, 
                COALESCE(SUM(quantity * price), 0) as total_value 
            FROM items
        ''')
        return self.c.fetchone()

    def get_categories(self):
        """Get list of all unique categories"""
        self.c.execute('SELECT DISTINCT category FROM items ORDER BY category')
        return [row[0] for row in self.c.fetchall()]

    def export_to_csv(self, filename):
        """Export database contents to CSV file"""
        try:
            self.c.execute('''
                SELECT code, name, quantity, price, category, notes
                FROM items
                ORDER BY name
            ''')
            
            rows = self.c.fetchall()
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(['Kode', 'Nama', 'Jumlah', 'Harga', 'Kategori', 'Catatan'])
                # Write data
                writer.writerows(rows)
                
            return len(rows)
        except Exception as e:
            raise Exception(f"Gagal ekspor data: {str(e)}")

    def import_from_csv(self, filename):
        """Import data from CSV file to database"""
        if not os.path.exists(filename):
            raise Exception(f"File {filename} tidak ditemukan")
            
        try:
            imported_count = 0
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                # Skip header row
                next(reader, None)
                
                for row in reader:
                    if len(row) >= 5:  # Ensure we have at least the required fields
                        code = row[0].strip()
                        name = row[1].strip()
                        
                        try:
                            quantity = int(row[2])
                        except ValueError:
                            quantity = 0
                            
                        try:
                            price = float(row[3])
                        except ValueError:
                            price = 0
                            
                        category = row[4].strip()
                        
                        # Handle notes field if exists
                        notes = row[5].strip() if len(row) > 5 else ""
                        
                        # Try to update first
                        self.c.execute('''
                            UPDATE items 
                            SET name=?, quantity=?, price=?, category=?, notes=?, updated_at=?
                            WHERE code=?
                        ''', (name, quantity, price, category, notes, current_time, code))
                        
                        # If not updated, insert
                        if self.c.rowcount == 0:
                            self.c.execute('''
                                INSERT INTO items (code, name, quantity, price, category, notes, created_at, updated_at)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (code, name, quantity, price, category, notes, current_time, current_time))
                            
                        imported_count += 1
            
            self.conn.commit()
            return imported_count
            
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Gagal impor data: {str(e)}")

    def backup_database(self, backup_file):
        """Create a backup of the database"""
        try:
            # Create a new connection to backup DB
            backup_conn = sqlite3.connect(backup_file)
            
            # Backup database
            with backup_conn:
                self.conn.backup(backup_conn)
                
            backup_conn.close()
            return True
        except Exception as e:
            raise Exception(f"Gagal membuat backup: {str(e)}")

    def restore_database(self, backup_file):
        """Restore database from backup file"""
        if not os.path.exists(backup_file):
            raise Exception(f"File backup {backup_file} tidak ditemukan")
            
        try:
            # Create a new connection to backup DB
            backup_conn = sqlite3.connect(backup_file)
            
            # Close current connection
            self.conn.close()
            
            # Delete current database and replace with backup
            os.remove(self.db_name)
            
            # Restore from backup
            with backup_conn:
                backup_conn.backup(self.conn)
                
            backup_conn.close()
            
            # Reopen connection
            self.conn = sqlite3.connect(self.db_name)
            self.c = self.conn.cursor()
            
            return True
        except Exception as e:
            raise Exception(f"Gagal restore database: {str(e)}")

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()