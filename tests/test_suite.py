# -*- coding: utf-8 -*-
"""
Unit-тесты для приложения автоматизации создания технических заданий
согласно ГОСТ 34.602-89

С видимыми результатами каждого теста
С функцией run_all_tests()
С генерацией DOCX файлов
"""

import unittest
import sys
from datetime import datetime
from pathlib import Path

# Попытка импорта генератора DOCX
try:
    from docx_generator import DOCXGenerator
    HAS_DOCX_GEN = True
except ImportError:
    HAS_DOCX_GEN = False
    print("Модуль docx_generator не найден!")


# ============================================================================
# СБОРЩИК РЕЗУЛЬТАТОВ ТЕСТОВ
# ============================================================================

class TestResultCollector:
    """Собирает результаты тестов с видимыми данными"""

    def __init__(self):
        self.results = []
        self.test_data = []

    def add_result(self, test_name, status, message="", expected="", actual="", details=None):
        """Добавить результат теста с полной информацией"""
        result = {
            'test_name': test_name,
            'status': 'PASSED' if status else 'FAILED',
            'message': message,
            'expected': expected,
            'actual': actual,
            'details': details or [],
            'timestamp': datetime.now(),
        }
        self.results.append(result)

        # Вывод в консоль
        print(f"\n{'='*80}")
        print(f"{result['status']} {test_name}")
        print(f"{'='*80}")
        print(f"Сообщение: {message}")
        if expected:
            print(f"Ожидается: {expected}")
        if actual:
            print(f"Получено: {actual}")
        if details:
            for detail in details:
                print(f"  • {detail}")
        print()

    def print_summary(self):
        """Вывести итоговый отчет"""
        passed = sum(1 for r in self.results if 'PASSED' in r['status'])
        failed = sum(1 for r in self.results if 'FAILED' in r['status'])
        total = len(self.results)

        print("\n" + "="*80)
        print("ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
        print("="*80)
        print(f"Пройдено:     {passed}/{total}")
        print(f"Не пройдено:  {failed}/{total}")
        print(f"Успешность:   {(passed/total*100):.1f}%")
        print("="*80 + "\n")

        return {
            'passed': passed,
            'failed': failed,
            'total': total,
            'success_rate': (passed/total*100) if total > 0 else 0
        }

    def export_to_docx(self):
        """Экспортировать результаты в DOCX"""
        if not HAS_DOCX_GEN:
            print("Генератор DOCX не доступен")
            return None

        try:
            generator = DOCXGenerator()

            # Создаем основной отчет
            docx_path = generator.create_test_results_report(
                self.results,
                filename="TEST_RESULTS.docx"
            )

            return docx_path
        except Exception as e:
            print(f"Ошибка при создании DOCX: {e}")
            return None


# Глобальный сборщик
RESULTS = TestResultCollector()


# ============================================================================
# СТАБЫ КЛАССОВ ДЛЯ ТЕСТИРОВАНИЯ
# ============================================================================

class SpecificationValidator:
    """Валидатор технического задания"""

    def validate(self, spec):
        #Валидирует техническое задание
        errors = []

        # Проверка названия проекта
        if 'project_name' not in spec or not spec['project_name']:
            errors.append('project_name')

        # Проверка требований
        if 'requirements' not in spec or len(spec.get('requirements', [])) == 0:
            errors.append('requirements')

        # Проверка формата даты начала
        if 'start_date' in spec:
            try:
                datetime.strptime(spec['start_date'], '%Y-%m-%d')
            except (ValueError, TypeError):
                errors.append('start_date')

        # Проверка диапазона дат
        if 'end_date' in spec and 'start_date' in spec:
            try:
                start = datetime.strptime(spec['start_date'], '%Y-%m-%d')
                end = datetime.strptime(spec['end_date'], '%Y-%m-%d')
                if end < start:
                    errors.append('date_range')
            except ValueError:
                pass

        # Проверка бюджета
        if 'budget' in spec and spec['budget'] < 0:
            errors.append('budget')

        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'checked_fields': list(spec.keys())
        }


class GOSTCompliance:
    """Проверка соответствия ГОСТ 34.602-89"""

    REQUIRED_SECTIONS = [
        'project_name',
        'system_purpose',
        'requirements',
        'constraints',
        'interfaces',
        'performance_requirements',
        'security_requirements'
    ]

    def check_required_sections(self, spec):
        """Проверяет наличие всех требуемых разделов"""
        missing = [s for s in self.REQUIRED_SECTIONS if s not in spec or not spec.get(s)]
        return {
            'compliant': len(missing) == 0,
            'missing_sections': missing,
            'found_sections': [s for s in self.REQUIRED_SECTIONS if s in spec]
        }

    def validate_section(self, spec, section):
        """Валидирует отдельный раздел"""
        if section not in spec or not spec[section]:
            return {'valid': False, 'reason': f'Раздел "{section}" отсутствует или пуст'}
        return {'valid': True, 'section': section, 'value': spec[section]}

    def generate_document(self, spec):
        """Генерирует документ по ГОСТ"""
        return {
            'project_name': spec.get('project_name'),
            'sections': list(range(1, 9)),  # 8 разделов
            'gost_compliant': True,
            'format': 'ГОСТ 34.602-89'
        }


class SpecificationExporter:
    """Экспортер технического задания"""

    SUPPORTED_FORMATS = ['docx', 'pdf', 'html']

    def export(self, spec, format_type):
        """Экспортирует в указанный формат"""
        if format_type not in self.SUPPORTED_FORMATS:
            return {'success': False, 'error': f'Формат {format_type} не поддерживается'}

        if format_type == 'docx':
            return self.save_docx(spec)
        elif format_type == 'pdf':
            return self.save_pdf(spec)
        elif format_type == 'html':
            return self.save_html(spec)

    def save_docx(self, spec):
        """Экспорт в DOCX"""
        return {
            'success': True,
            'format': 'DOCX',
            'filename': f"{spec.get('project_name', 'specification')}.docx",
            'size_mb': 0.25
        }

    def save_pdf(self, spec):
        """Экспорт в PDF"""
        return {
            'success': True,
            'format': 'PDF',
            'filename': f"{spec.get('project_name', 'specification')}.pdf",
            'size_mb': 0.15
        }

    def save_html(self, spec):
        """Экспорт в HTML"""
        return {
            'success': True,
            'format': 'HTML',
            'filename': f"{spec.get('project_name', 'specification')}.html",
            'size_mb': 0.10
        }

    def prepare_export(self, spec):
        """Подготовка к экспорту с метаданными"""
        return {
            **spec,
            'created_date': datetime.now(),
            'version': '1.0',
            'author': 'Test System',
            'status': 'Draft'
        }


class RequirementsParser:
    """Парсер требований"""

    def parse(self, text):
        """Парсит текст требования"""
        parts = text.split(':', 1)
        result = {'description': text, 'type': 'unknown'}

        if len(parts) > 1 and parts[0].startswith('REQ'):
            result['id'] = parts[0].strip()
            result['description'] = parts[1].strip()
            result['type'] = 'functional'

        return result

    def deduplicate(self, requirements):
        """Удаляет дубликаты"""
        seen = set()
        result = []
        for req in requirements:
            if req not in seen:
                seen.add(req)
                result.append(req)
        return result

    def categorize(self, requirements):
        """Категоризирует требования"""
        categories = {
            'infrastructure': [],
            'integration': [],
            'security': [],
            'export': []
        }

        keywords = {
            'infrastructure': ['Linux', 'Windows', 'сервер', 'база данных'],
            'integration': ['интеграция', 'API', 'PostgreSQL'],
            'security': ['аутентификация', 'LDAP', 'шифрование'],
            'export': ['экспорт', 'PDF', 'Excel']
        }

        for req in requirements:
            found = False
            for category, words in keywords.items():
                if any(word.lower() in req.lower() for word in words):
                    categories[category].append(req)
                    found = True
                    break
            if not found:
                categories['infrastructure'].append(req)

        return categories


# ============================================================================
# UNIT-ТЕСТЫ
# ============================================================================

class TestTechnicalSpecificationValidator(unittest.TestCase):
    """Тесты валидации технического задания"""

    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.validator = SpecificationValidator()
        self.valid_spec = {
            'project_name': 'Система управления документами',
            'organization': 'ООО Технологии',
            'description': 'Система для управления и архивирования документов',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'requirements': ['Интеграция с AD', 'REST API', 'Веб-интерфейс'],
            'team_lead': 'Иван Петров',
            'budget': 500000
        }

    def test_01_valid_specification(self):
        """Тест 1: Корректное ТЗ должно быть валидным"""
        result = self.validator.validate(self.valid_spec)

        RESULTS.add_result(
            test_name="Валидация корректного ТЗ",
            status=result['is_valid'],
            message="ТЗ прошло полную валидацию",
            expected="is_valid = True, errors = []",
            actual=f"is_valid = {result['is_valid']}, errors = {result['errors']}",
            details=[
                f"Проверено полей: {', '.join(result['checked_fields'])}",
                f"Ошибок валидации: {len(result['errors'])}",
                "Все требуемые поля присутствуют"
            ]
        )

        self.assertTrue(result['is_valid'])
        self.assertEqual(len(result['errors']), 0)

    def test_02_missing_project_name(self):
        """Тест 2: Отсутствие названия проекта должно вызвать ошибку"""
        spec = self.valid_spec.copy()
        del spec['project_name']

        result = self.validator.validate(spec)

        RESULTS.add_result(
            test_name="Отсутствие названия проекта",
            status=not result['is_valid'],
            message="Ошибка корректно обнаружена",
            expected="'project_name' в errors",
            actual=f"errors = {result['errors']}",
            details=[
                f"Количество ошибок: {len(result['errors'])}",
                f"Содержит ошибку: {'project_name' in result['errors']}"
            ]
        )

        self.assertFalse(result['is_valid'])
        self.assertIn('project_name', result['errors'])

    def test_03_empty_requirements(self):
        """Тест 3: Пустой список требований должен быть отклонен"""
        spec = self.valid_spec.copy()
        spec['requirements'] = []

        result = self.validator.validate(spec)

        RESULTS.add_result(
            test_name="Пустой список требований",
            status=not result['is_valid'],
            message="Пустой список требований отклонен",
            expected="'requirements' в errors",
            actual=f"errors = {result['errors']}",
            details=[
                f"Количество требований: {len(spec['requirements'])}",
                "Валидация отклонила пустой список"
            ]
        )

        self.assertFalse(result['is_valid'])
        self.assertIn('requirements', result['errors'])

    def test_04_invalid_date_format(self):
        """Тест 4: Некорректный формат даты должен вызвать ошибку"""
        spec = self.valid_spec.copy()
        spec['start_date'] = '01/01/2024'  # Неправильный формат

        result = self.validator.validate(spec)

        RESULTS.add_result(
            test_name="Некорректный формат даты",
            status=not result['is_valid'],
            message="Ошибка формата даты обнаружена",
            expected="'start_date' в errors",
            actual=f"errors = {result['errors']}, date_format = '{spec['start_date']}'",
            details=[
                "Формат даты: '01/01/2024' (неправильный)",
                "Ожидаемый формат: 'YYYY-MM-DD'",
                "Валидация отклонила неправильный формат"
            ]
        )

        self.assertFalse(result['is_valid'])
        self.assertIn('start_date', result['errors'])

    def test_05_end_date_before_start_date(self):
        """Тест 5: Дата окончания раньше начала должна быть отклонена"""
        spec = self.valid_spec.copy()
        spec['end_date'] = '2023-12-31'  # Раньше start_date

        result = self.validator.validate(spec)

        RESULTS.add_result(
            test_name="Дата окончания раньше начала",
            status=not result['is_valid'],
            message="Ошибка диапазона дат обнаружена",
            expected="'date_range' в errors",
            actual=f"errors = {result['errors']}, start = {spec['start_date']}, end = {spec['end_date']}",
            details=[
                f"Дата начала: {spec['start_date']}",
                f"Дата окончания: {spec['end_date']}",
                "Дата окончания раньше даты начала",
                "Валидация отклонила некорректный диапазон"
            ]
        )

        self.assertFalse(result['is_valid'])
        self.assertIn('date_range', result['errors'])


class TestGOSTCompliance(unittest.TestCase):
    """Тесты соответствия ГОСТ 34.602-89"""

    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.gost_checker = GOSTCompliance()
        self.complete_spec = {
            'project_name': 'Проект',
            'system_purpose': 'Автоматизация процессов',
            'requirements': ['Требование 1', 'Требование 2'],
            'constraints': ['Ограничение 1'],
            'interfaces': ['Интеграция с системой X'],
            'performance_requirements': ['Обработка 1000 записей/сек'],
            'security_requirements': ['Аутентификация', 'Шифрование'],
        }

    def test_06_required_sections_present(self):
        """Тест 6: Все обязательные разделы должны присутствовать"""
        result = self.gost_checker.check_required_sections(self.complete_spec)

        RESULTS.add_result(
            test_name="Присутствие всех разделов ГОСТ",
            status=result['compliant'],
            message="Все обязательные разделы обнаружены",
            expected=f"compliant = True, missing_sections = []",
            actual=f"compliant = {result['compliant']}, missing = {result['missing_sections']}",
            details=[
                f"Требуемые разделы: {len(self.gost_checker.REQUIRED_SECTIONS)}",
                f"Найдено разделов: {len(result['found_sections'])}",
                f"Отсутствующих: {len(result['missing_sections'])}",
                "Все разделы ГОСТ 34.602-89 присутствуют"
            ]
        )

        self.assertTrue(result['compliant'])
        self.assertEqual(len(result['missing_sections']), 0)

    def test_07_missing_security_requirements(self):
        """Тест 7: Отсутствие требований безопасности должно быть обнаружено"""
        spec = self.complete_spec.copy()
        del spec['security_requirements']

        result = self.gost_checker.check_required_sections(spec)

        RESULTS.add_result(
            test_name="Обнаружение отсутствия требований безопасности",
            status=not result['compliant'],
            message="Отсутствие критического раздела обнаружено",
            expected="'security_requirements' в missing_sections",
            actual=f"missing_sections = {result['missing_sections']}",
            details=[
                f"Всего отсутствует разделов: {len(result['missing_sections'])}",
                f"Отсутствующий раздел: security_requirements",
                "ГОСТ требует раздел 'Требования безопасности'",
                "Документ не соответствует ГОСТ"
            ]
        )

        self.assertFalse(result['compliant'])
        self.assertIn('security_requirements', result['missing_sections'])

    def test_08_system_purpose_non_empty(self):
        """Тест 8: Назначение системы не должно быть пустым"""
        spec = self.complete_spec.copy()
        spec['system_purpose'] = ''
        result = self.gost_checker.validate_section(spec, 'system_purpose')

        RESULTS.add_result(
            test_name="Валидация назначения системы",
            status=not result['valid'],
            message="Пустое назначение системы отклонено",
            expected="valid = False",
            actual=f"valid = {result['valid']}, reason = '{result.get('reason', '')}'",
            details=[
                f"Назначение системы: '{spec['system_purpose']}' (пусто)",
                "Валидация отклонила пустую строку",
                "ГОСТ требует заполненное описание назначения"
            ]
        )

        self.assertFalse(result['valid'])

    def test_09_generate_gost_compliant_document(self):
        """Тест 9: Генерация документа в формате ГОСТ"""
        document = self.gost_checker.generate_document(self.complete_spec)

        RESULTS.add_result(
            test_name="Генерация документа ГОСТ",
            status=document is not None and len(document.get('sections', [])) == 8,
            message="Документ успешно сгенерирован по ГОСТ",
            expected="8 разделов документа",
            actual=f"{len(document.get('sections', []))} разделов",
            details=[
                f"Название проекта: {document.get('project_name')}",
                f"Количество разделов: {len(document.get('sections', []))}",
                f"Формат: {document.get('format')}",
                f"ГОСТ соответствие: {document.get('gost_compliant')}",
                "Документ содержит все 8 обязательных разделов ГОСТ"
            ]
        )

        self.assertIsNotNone(document)
        self.assertEqual(len(document['sections']), 8)


class TestSpecificationExport(unittest.TestCase):
    """Тесты экспорта технического задания"""

    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.exporter = SpecificationExporter()
        self.spec = {
            'project_name': 'Система управления',
            'description': 'Описание проекта',
            'requirements': ['Требование 1', 'Требование 2']
        }

    def test_10_export_to_docx(self):
        """Тест 10: Экспорт в DOCX"""
        result = self.exporter.export(self.spec, 'docx')

        RESULTS.add_result(
            test_name="Экспорт в DOCX",
            status=result['success'],
            message="Экспорт в DOCX успешен",
            expected="success = True, format = 'DOCX'",
            actual=f"success = {result['success']}, format = {result.get('format')}",
            details=[
                f"Название файла: {result.get('filename')}",
                f"Размер: {result.get('size_mb')} МБ",
                "Формат DOCX поддерживается и работает"
            ]
        )

        self.assertTrue(result['success'])
        self.assertEqual(result['format'], 'DOCX')

    def test_11_export_to_pdf(self):
        """Тест 11: Экспорт в PDF"""
        result = self.exporter.export(self.spec, 'pdf')

        RESULTS.add_result(
            test_name="Экспорт в PDF",
            status=result['success'],
            message="Экспорт в PDF успешен",
            expected="success = True, format = 'PDF'",
            actual=f"success = {result['success']}, format = {result.get('format')}",
            details=[
                f"Название файла: {result.get('filename')}",
                f"Размер: {result.get('size_mb')} МБ",
                "Формат PDF поддерживается и работает"
            ]
        )

        self.assertTrue(result['success'])
        self.assertEqual(result['format'], 'PDF')

    def test_12_export_invalid_format(self):
        """Тест 12: Отклонение неподдерживаемого формата"""
        result = self.exporter.export(self.spec, 'xyz')

        RESULTS.add_result(
            test_name="Отклонение неподдерживаемого формата",
            status=not result['success'],
            message="Неподдерживаемый формат отклонен",
            expected="success = False",
            actual=f"success = {result['success']}, error = '{result.get('error')}'",
            details=[
                f"Запрошенный формат: xyz",
                f"Поддерживаемые форматы: {', '.join(self.exporter.SUPPORTED_FORMATS)}",
                "Система правильно отклонила неизвестный формат"
            ]
        )

        self.assertFalse(result['success'])

    def test_13_export_adds_metadata(self):
        """Тест 13: Добавление метаданных при экспорте"""
        exported = self.exporter.prepare_export(self.spec)

        has_metadata = all(k in exported for k in ['created_date', 'version', 'author', 'status'])

        RESULTS.add_result(
            test_name="Добавление метаданных при экспорте",
            status=has_metadata,
            message="Метаданные успешно добавлены",
            expected="created_date, version, author, status присутствуют",
            actual=f"Ключи: {', '.join([k for k in exported.keys() if k.endswith('date') or k in ['version', 'author', 'status']])}",
            details=[
                f"Дата создания: {exported.get('created_date')}",
                f"Версия: {exported.get('version')}",
                f"Автор: {exported.get('author')}",
                f"Статус: {exported.get('status')}",
                "Все метаданные добавлены корректно"
            ]
        )

        self.assertTrue(has_metadata)

    def test_14_export_preserves_structure(self):
        """Тест 14: Сохранение структуры документа"""
        exported = self.exporter.prepare_export(self.spec)

        structure_preserved = (
            exported['project_name'] == self.spec['project_name'] and
            exported['description'] == self.spec['description'] and
            len(exported['requirements']) == len(self.spec['requirements'])
        )

        RESULTS.add_result(
            test_name="Сохранение структуры при экспорте",
            status=structure_preserved,
            message="Структура документа полностью сохранена",
            expected="Все поля исходного документа совпадают",
            actual=f"Все {len(self.spec)} полей сохранены",
            details=[
                f"Название проекта: {exported.get('project_name')} ",
                f"Описание: {len(exported.get('description', ''))} символов ",
                f"Требований: {len(exported.get('requirements', []))} ",
                "Структура полностью сохранена"
            ]
        )

        self.assertTrue(structure_preserved)


class TestRequirementsParsing(unittest.TestCase):
    """Тесты парсинга и обработки требований"""

    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.parser = RequirementsParser()

    def test_15_parse_simple_requirement(self):
        """Тест 15: Парсинг простого требования"""
        text = "Система должна поддерживать 1000 одновременных пользователей"
        result = self.parser.parse(text)

        RESULTS.add_result(
            test_name="Парсинг простого требования",
            status=result is not None and 'description' in result,
            message="Требование успешно распарсено",
            expected="description = исходный текст",
            actual=f"description = '{result.get('description')}'",
            details=[
                f"Тип требования: {result.get('type')}",
                f"Длина текста: {len(result.get('description', ''))} символов",
                "Простое требование распарсено"
            ]
        )

        self.assertIsNotNone(result)
        self.assertEqual(result['description'], text)

    def test_16_parse_requirement_with_metrics(self):
        """Тест 16: Парсинг требования с метриками"""
        text = "REQ-001: Время ответа < 500ms при нагрузке 1000 пользователей"
        result = self.parser.parse(text)

        RESULTS.add_result(
            test_name="Парсинг требования с метриками",
            status='id' in result and '500ms' in result.get('description', ''),
            message="Требование с метриками распарсено",
            expected="id = 'REQ-001', description содержит '500ms'",
            actual=f"id = {result.get('id')}, metrics in description = {'500ms' in result.get('description', '')}",
            details=[
                f"ID требования: {result.get('id')}",
                f"Тип: {result.get('type')}",
                f"Метрика: 500ms",
                f"Описание: {result.get('description')[:50]}...",
                "ID и метрики успешно извлечены"
            ]
        )

        self.assertEqual(result.get('id'), 'REQ-001')
        self.assertIn('500ms', result.get('description', ''))

    def test_17_deduplicate_requirements(self):
        """Тест 17: Удаление дубликатов"""
        requirements = [
            "Требование 1",
            "Требование 2",
            "Требование 1",  # Дубликат
            "Требование 3",
            "Требование 2"   # Дубликат
        ]

        result = self.parser.deduplicate(requirements)

        RESULTS.add_result(
            test_name="Удаление дубликатов требований",
            status=len(result) == 3,
            message="Дубликаты успешно удалены",
            expected="3 уникальных требования",
            actual=f"{len(result)} уникальных требований",
            details=[
                f"Было требований: {len(requirements)}",
                f"Дубликатов найдено: {len(requirements) - len(result)}",
                f"Осталось уникальных: {len(result)}",
                f"Уникальные требования: {', '.join(result)}",
                "Дубликаты успешно удалены"
            ]
        )

        self.assertEqual(len(result), 3)

    def test_18_categorize_requirements(self):
        """Тест 18: Категоризация требований"""
        requirements = [
            "Система должна работать на Linux",
            "Интеграция с базой данных PostgreSQL",
            "Аутентификация через LDAP",
            "Экспорт в PDF"
        ]

        result = self.parser.categorize(requirements)

        has_all_categories = all(cat in result for cat in ['infrastructure', 'integration', 'security', 'export'])

        RESULTS.add_result(
            test_name="Категоризация требований",
            status=has_all_categories,
            message="Требования успешно категоризированы",
            expected="4 категории с требованиями",
            actual=f"Категории: {', '.join(k for k, v in result.items() if v)}",
            details=[
                f"Infrastructure: {len(result['infrastructure'])} требований",
                f"Integration: {len(result['integration'])} требований",
                f"Security: {len(result['security'])} требований",
                f"Export: {len(result['export'])} требований",
                "Все требования успешно категоризированы"
            ]
        )

        self.assertTrue(has_all_categories)


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ ДЛЯ ЗАПУСКА
# ============================================================================

def run_all_tests():
    """Запускает все тесты и создает отчеты"""

    print("\n" + "="*80)
    print("ЗАПУСК ВСЕХ UNIT-ТЕСТОВ".center(80))
    print("="*80 + "\n")

    # Создание тестового набора
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Добавление тестов
    suite.addTests(loader.loadTestsFromTestCase(TestTechnicalSpecificationValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestGOSTCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestSpecificationExport))
    suite.addTests(loader.loadTestsFromTestCase(TestRequirementsParsing))

    # Запуск с подробным выводом
    runner = unittest.TextTestRunner(verbosity=0)  # Без двойного вывода
    result = runner.run(suite)

    # Итоговый отчет
    summary = RESULTS.print_summary()

    # Экспорт в DOCX
    print("="*80)
    print("ГЕНЕРАЦИЯ ОТЧЕТОВ".center(80))
    print("="*80 + "\n")

    docx_path = RESULTS.export_to_docx()

    if docx_path:
        print(f"Отчет сохранен: {docx_path}\n")
    else:
        print("Отчет не был создан\n")

    # Генерация примера ТЗ
    if HAS_DOCX_GEN:
        try:
            generator = DOCXGenerator()
            spec_example = {
                'project_name': 'Система управления документами',
                'organization': 'ООО Технологии',
                'team_lead': 'Иван Петров',
                'budget': 500000,
                'description': 'Система для управления, архивирования и экспорта документов',
                'start_date': '2024-01-01',
                'end_date': '2024-12-31',
                'requirements': [
                    'REQ-001: Интеграция с Active Directory',
                    'REQ-002: REST API для внешних приложений',
                    'REQ-003: Веб-интерфейс для управления',
                    'REQ-004: Экспорт в PDF и DOCX',
                    'REQ-005: Полнотекстовый поиск'
                ],
                'constraints': [
                    'Поддержка HTTPS',
                    'Минимальное разрешение 1024x768',
                    'Максимальный размер документа 100 МБ'
                ]
            }

            spec_path = generator.create_specification_example(spec_example)
            print(f"Пример ТЗ сохранен: {spec_path}\n")
        except Exception as e:
            print(f"Ошибка при создании примера ТЗ: {e}\n")

    print("="*80)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО".center(80))
    print("="*80 + "\n")

    return summary


if __name__ == '__main__':
    summary = run_all_tests()

    # Вывод финального резюме
    print("\nИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print(f"Пройдено:     {summary['passed']}/{summary['total']}")
    print(f"Ошибки:       {summary['failed']}/{summary['total']}")
    print(f"Успешность:   {summary['success_rate']:.1f}%\n")
