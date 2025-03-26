from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest
import unittest
import json

app = Flask(name)

# 1. Функция для вычисления первых n факториалов
def factorial(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def first_n_factorials(n):
    if n < 1:
        raise ValueError("n must be a positive integer")
    return [factorial(i) for i in range(n)]

# 2. Функция для удаления дубликатов из списка
def remove_duplicates(input_list):
    if not isinstance(input_list, list):
        raise TypeError("Input must be a list")
    return list(set(input_list))

# 3. Класс для узла связного списка и функция для его разворота
class ListNode:
    def init(self, value=0, next=None):
        self.value = value
        self.next = next

def reverse_linked_list(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_linked_list(head.next)
    head.next.next = head
    head.next = None
    return new_head

# REST API Endpoints
@app.route('/factorials', methods=['GET'])
def get_factorials():
    try:
        n = int(request.args.get('n'))
        result = first_n_factorials(n)
        return jsonify(result), 200
    except ValueError as e:
        raise BadRequest(str(e))

@app.route('/remove_duplicates', methods=['POST'])
def remove_duplicates_endpoint():
    try:
        input_list = request.json.get('list')
        result = remove_duplicates(input_list)
        return jsonify(result), 200
    except (TypeError, KeyError) as e:
        raise BadRequest(str(e))

@app.route('/reverse_linked_list', methods=['POST'])
def reverse_linked_list_endpoint():
    try:
        values = request.json.get('list')
        if not values or not isinstance(values, list):
            raise ValueError("Input must be a list of values")
        
        # Создание связного списка
        head = ListNode(values[0])
        current = head
        for value in values[1:]:
            current.next = ListNode(value)
            current = current.next
        
        # Разворот списка
        reversed_head = reverse_linked_list(head)
        
        # Преобразование обратно в список для ответа
        reversed_list = []
        while reversed_head:
            reversed_list.append(reversed_head.value)
            reversed_head = reversed_head.next
        
        return jsonify(reversed_list), 200
    except ValueError as e:
        raise BadRequest(str(e))

# Unit Tests
class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_get_factorials(self):
        response = self.app.get('/factorials?n=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [1, 1, 2, 6, 24])
    
    def test_remove_duplicates_endpoint(self):
        response = self.app.post('/remove_duplicates', json={'list': [1, 2, 2, 3]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [1, 2, 3])

    def test_reverse_linked_list_endpoint(self):
        response = self.app.post('/reverse_linked_list', json={'list': [1, 2, 3]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [3, 2, 1])

if name == 'main':
    # Запуск сервера
    app.run(debug=True)

    # Запуск тестов (можно закомментировать эту часть при запуске сервера)
    # unittest.main()
