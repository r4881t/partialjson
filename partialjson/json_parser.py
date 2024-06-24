import json
import re

class JSONParser:
    def __init__(self):
        self.parsers = {
            ' ': self.parse_space,
            '\r': self.parse_space,
            '\n': self.parse_newline,
            '\\n': self.parse_newline,
            '\t': self.parse_space,
            '[': self.parse_array,
            '{': self.parse_object,
            '"': self.parse_string,
            't': self.parse_true,
            'f': self.parse_false,
            'n': self.parse_null
        }
        # Adding parsers for numbers
        for c in '0123456789.-':
            self.parsers[c] = self.parse_number

        self.last_parse_reminding = None
        self.on_extra_token = self.default_on_extra_token

    def clean_json_string(self, input_string):
        # Remove markdown code block syntax if present
        clean_string = input_string.strip('```json\n').rstrip('\n```')
        # Trim and return
        clean_string = clean_string.strip()
        # Convert \n to \\n
        clean_string = clean_string.replace('\n', '\\n')
        return clean_string

    def default_on_extra_token(self, text, data, reminding):
        print('Parsed JSON with extra tokens:', {'text': text, 'data': data, 'reminding': reminding})

    def parse(self, s):
        s = s.strip()  # Strip whitespace before starting
        s = self.clean_json_string(s)
        if s:
            try:
                return json.loads(s)
            except json.JSONDecodeError as e:
                data, reminding = self.parse_any(s, e)
                self.last_parse_reminding = reminding
                if self.on_extra_token and reminding:
                    self.on_extra_token(s, data, reminding)
                return json.loads(json.dumps(data))
        else:
            return json.loads("{}")

    def parse_any(self, s, e):
        if not s:
            raise e
        parser = self.parsers.get(s[0])
        if not parser:
            attempt2 = s[:2]
            parser = self.parsers.get(attempt2)
            if not parser:
              raise e
        return parser(s, e)

    def parse_newline(self, s, e):
        if s.startswith('\\n'):
            s = s[2:].strip()
        elif s.startswith('\n'):
            s = s[1:].strip()
        return self.parse_any(s, e)
        # s = s.lstrip()
        # return self.parse_any(s, e)

    def parse_space(self, s, e):
        s = s.lstrip()  # Strip leading spaces
        return self.parse_any(s, e)

    def parse_array(self, s, e):
        s = s[1:].strip()  # Skip '[' and strip
        # Remove any \n," kind of characters

        s = re.sub(r',\\n\s*"', ',"', s)
        s = re.sub(r'\\n\s*"', '"', s)
        s = re.sub(r'"\s*\\n\s*]', '"]', s)
        acc = []
        while s and s[0] != ']':
            res, s = self.parse_any(s, e)
            acc.append(res)
            s = s.strip()  # Strip after processing each element
            if s.startswith(','):
                s = s[1:].strip()
        if s.startswith(']'):
            s = s[1:].strip()
        return acc, s

    def parse_object(self, s, e):
        s = s[1:].strip()  # Skip '{' and strip
        s = s.replace('\\n}', '}')
        acc = {}
        while s and s[0] != '}':
            key, s = self.parse_any(s, e)
            s = s.strip()
            if s.startswith(':'):
                s = s[1:].strip()
                if s and s[0] in ',}':
                    value = None
                else:
                    value, s = self.parse_any(s, e)
                acc[key] = value
                s = s.strip()
                if s.startswith(','):
                    s = s[1:].strip()
            else:
                acc[key] = None
        if s.startswith('}'):
            s = s[1:].strip()
        return acc, s

    # Other parse methods like parse_string, parse_number, parse_true, parse_false, parse_null should remain the same.
    def parse_string(self, s, e):
      end = s.find('"', 1)
      while end != -1 and s[end - 1] == '\\':  # Correctly handle escaped quotes
          end = s.find('"', end + 1)
      if end == -1:
          raise e  # Error if the string is incomplete
      # Extract the string including the quotes for proper JSON loading
      str_val = s[:end + 1]
      s = s[end + 1:].strip()
      return json.loads(str_val), s

    def parse_number(self, s, e):
        i = 0
        while i < len(s) and s[i] in '0123456789+-eE.':
            i += 1
        num_str = s[:i]
        s = s[i:].strip()  # Strip after reading number
        if not num_str or num_str in "+-.":
            raise e  # Raise error if number is invalid
        try:
            if '.' in num_str or 'e' in num_str or 'E' in num_str:
                num = float(num_str)
            else:
                num = int(num_str)
        except ValueError:
            raise e  # Raise error if conversion fails
        return num, s

    def parse_true(self, s, e):
        if s.startswith('true') or s.startswith('True'):
            return True, s[4:].strip()  # Strip after 'true'
        raise e  # Raise error if 'true' is malformed

    def parse_false(self, s, e):
        if s.startswith('false') or s.startswith('False'):
            return False, s[5:].strip()  # Strip after 'false'
        raise e  # Raise error if 'false' is malformed

    def parse_null(self, s, e):
        if s.startswith('null') or s.startswith('Null'):
            return None, s[4:].strip()  # Strip after 'null'
        raise e  # Raise error if 'null' is malformed
