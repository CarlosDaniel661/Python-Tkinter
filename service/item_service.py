import json
import os
from datetime import datetime


class ItemService:
    def __init__(self, filename='tasks.json'):
        self.filename =filename
        self.items = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return {}
    
    def save_task(self):
        with open(self.filename, 'w') as file:
            json.dump(self.items, file, indent=4)
    
    def get_items(self, date_str):
        return self.items.get(date_str,[])
    
    def add_item(self, date_str, task):
        if date_str in self.items:
            self.items[date_str].append(task)
        else:
            self.items[date_str] = [task]
        self.save_task()

    def update_item(self, date_str, index, new_task):
        if date_str in self.items and 0 <= index < len(self.items[date_str]):
            self.items[date_str][index] = new_task
            self.save_task()

    def get_all_items(self):
        all_tasks = []
        for date_str, tasks in self.items.items():
            for task in tasks:
                all_tasks.append((task, date_str))
        return all_tasks