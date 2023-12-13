'''
Class to divide text if it passes the maximum number of bytes, respecting the
length of the words, it does not cut them.
'''


class TextWrapper:
    '''
    Class to divide text by string of 500 characters respecting words.

    Returns a list of text strings respecting the maximum bytes of the API.
    '''
    ending_text = ['.', ',', ';', ':']  # determines end of paragraph
    limit = 500    # constant
    start_index = 0
    last_index = limit

    def __init__(
        self,
        chars_limit: int = limit
    ) -> None:
        '''
        Constructor, `chars_limit` set limit to split bytes of text.
        '''
        self.limit = chars_limit

    def __text_wrapper(
        self,
        array_bytes: bytearray
    ) -> int:
        '''
        Search for the end of the text using `ending_text` characters.
        '''
        i = -1
        while abs(i) < len(array_bytes):
            if chr(array_bytes[i]) in self.ending_text:
                break
            i -= 1
        return i + 1

    def wrap(
        self,
        text: str
    ) -> dict:
        '''
        Handles division of text by words. Main function.

        Returns:
                    list: list of string with text splitted.
        '''
        result = []
        text_size = 0
        if len(self.__to_bytes(text)) <= 500:
            text_size += len(text)
            result.append(text)
        else:
            while True:
                chunk = self.__to_bytes(
                    text=text.strip(),
                    start=self.start_index,
                    end=self.last_index
                )

                if len(chunk) <= 0:
                    break
                index = self.__text_wrapper(array_bytes=chunk)

                chunk_last = chunk[0: self.limit + index]

                text_size += len(chunk_last)
                result.append(self.__to_string(chunk_last))

                self.start_index += len(chunk_last)
                self.last_index += len(chunk_last)

        self.__clear()
        return {
            'result': result,
            'text_size': text_size
        }

    def __clear(self) -> None:
        '''
        Clear indexes to origin.
        '''
        self.start_index = 0
        self.last_index = self.limit

    def __to_bytes(
        self,
        text: str,
        start: int = 0,
        end: int = None
    ) -> bytearray:
        '''
        Convert string on array of bytes.
        '''
        x = bytearray(
                    text.strip(),
                    encoding='utf-8'
                )
        if end is not None:
            return x[start: end]
        else:
            return x

    def __to_string(
        self,
        arr_bytes: bytearray
    ) -> str:
        '''
        Convert array of bytes on string.
        '''
        return arr_bytes.decode('utf-8').strip()
