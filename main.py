from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from youtube_dl import YoutubeDL
import time
import os
import threading
#Arquivo principal
firefox_options = Options()
firefox_options.add_argument('--no-sandbox')
firefox_options.add_argument('--disable-dev-shm-usage')


class Marcia:
  """
  Class para instanciar a MARCIA.
  """

  def __init__(self, path=None):
    """
    indicar onde se encontra o arquivo chromedriver.exe ou geckodriver.exe para abrir o navegador.
    :param path: String
    """
    self.driver = webdriver.Firefox(options=firefox_options)

  def init_whats(self) -> None:
    """
    Inicia o webdriver, abrindo o navegador na página do whatsapp para ter
    o QR code lido.
    :return:
    """
    self.driver.get("http://web.whatsapp.com")

  def is_logged(self) -> bool:
      """
      Verifica se o QR code foi escaneado ou não.
      :return:
      """
      try:
          logado = self.driver.find_element_by_class_name("_3QfZd")
          if logado:
              return True
          else:
              return False
      except:
          return False

  def get_contacts_text(self) -> list:
      """
      Retorna o nome dos contatos que estão na tela principal
      :return: List
      """
      contatos = self.driver.find_elements_by_class_name("_2aBzC")
      contatos_text = [x.find_element_by_class_name("_35k-1").text for x in contatos]
      return contatos_text

  def get_contact_text(self, i: int) -> str:
      """
      Retorna o nome de um contato com base em seu index.
      :param i: Int
      :return: String
      """
      contatos = self.driver.find_elements_by_class_name("_2aBzC")
      contatos_text = [x.find_element_by_class_name("_35k-1").text for x in contatos]
      return contatos_text[i]

  def get_contacts_object(self) -> list:
      """
      Retorna uma lista contendo vários objetos do tipo webdriver
      :return: List of WebDrivers Object
      """
      contatos = self.driver.find_elements_by_class_name("_2aBzC")
      return contatos

  def get_contact_object(self, contact: str) -> webdriver:
      """
      Retorna um contato do tipo webdriver.
      :param contact: String
      :return: WebDriver Object
      """
      index = self.get_contacts_text().index(contact)
      return self.get_contacts_object()[index]

  def is_contact_object(self, contact: str) -> bool:
      """
      Verifica se um objeto do tipo contact existe, para isso ele verifica na lista de nomes de contatos
      :param contact: String
      :return: Bool
      """
      return contact in self.get_contacts_text()

  def select_chat(self) -> webdriver:
      """
      Retorna um objeto do tipo driver contendo suas funcionalidades.
      :return: WebDriver Object
      """
      div = self.driver.find_element_by_class_name("_2A8P4")
      chat = div.find_element_by_class_name("_2_1wd")
      return chat

  def close_overlays(self) -> None:
      """
      Fecha qualquer overlay que atrapalhe a continuação do código
      overlay: Uma imagem aberta.
      :return:
      """
      try:
          overlay = self.driver.find_element_by_class_name("_1sMV6")
          overlay.send_keys(Keys.ESCAPE)
          time.sleep(1)
      except:
          pass

  def send_message(self, contact: str, message: str) -> None:
      """
      Envia uma mensagem para o contato especificado.
      exemplo de chamada:
          send_message(Yoda, "Com você a força estará")
      :param contact: String
      :param message: String
      :return: None
      """
      if not self.is_contact_object(contact):
          return None
      contato = self.get_contact_object(contact)
      self.close_overlays()
      contato.click()
      chat = self.select_chat()
      chat.send_keys(message)
      chat.send_keys(Keys.RETURN)

  def contacts_with_messages_unread(self) -> list:
      """
      Retorna uma lista com os contatos que estão com mensagens que não estão lidas
      :return: list of contact text names
      """
      contatos = self.get_contacts_object()
      contatos_text = self.get_contacts_text()
      contatos_msg_unread = []
      for i, contato in enumerate(contatos):
          try:
              mensagem_nova = contato.find_element_by_class_name("_38M1B")
              if mensagem_nova:
                  contatos_msg_unread.append(contatos_text[i])
          except:
              pass
      return contatos_msg_unread

  def list_with_messages_unread(self) -> list:
      """
      Retorna lista das mensagens que não foram lidas
      :return: list of messages text
      """
      contacts_with_messages_unread = self.contacts_with_messages_unread()
      textos_n_lidos = []
      for contact in contacts_with_messages_unread:
          contato = self.get_contact_object(contact)
          texto = contato.find_elements_by_class_name("_35k-1")[1]
          textos_n_lidos.append(texto.text)
      return textos_n_lidos

  def list_with_contact_and_messages_unread(self) -> list:
      """
      Retorna uma lista de tuplas contendo como valor (contato, mensagem)
      :return: List
      """
      list_contact_and_message = [(contact, self.list_with_messages_unread()[i]) for i, contact in enumerate(
          self.contacts_with_messages_unread())]
      return list_contact_and_message

  def send_file(self, contact: str, path: str) -> None:
      """
      Envia um arquivo para o contato especificado
      :param contact: Strin
      :param path: String
      :return: None
      """
      if not self.is_contact_object(contact):
        return None
      contato = self.get_contact_object(contact)
      self.close_overlays()
      contato.click()
      footer = self.driver.find_element_by_tag_name("footer")
      file_input = footer.find_element_by_class_name("_2n-zq")
      file_input.click()
      file_div = file_input.find_element_by_class_name("_1pLAS")
      input_send = file_div.find_element_by_tag_name("input")
      input_send.send_keys(path)
      time.sleep(3)
      buttom_send = self.driver.find_element_by_class_name("_1sMV6")
      buttom_send = buttom_send.find_element_by_class_name("_3v5V7")
      buttom_send = buttom_send.find_element_by_tag_name("div")
      buttom_send.click()


def main():
  ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
      }],
  }
  nova_marcia = Marcia()
  music_down = YoutubeDL(ydl_opts)
  program = True

  def download_music(ctt, link):
      nova_marcia.send_message(ctt, "*(Elielson_bot)*: Iniciando donwload, aguarde alguns segundos!")
      music_down.download([link])
      nova_marcia.send_message(ctt, "*(Elielson_bot)*: Arquivo baixado!")
      arquivo = [x for x in os.listdir("./musicas") if x.endswith("{}.mp3".format(ctt))][0]
      nova_marcia.send_file(ctt, os.path.abspath("./musicas/{}".format(arquivo)))

  while program:

    if not nova_marcia.is_logged():
      nova_marcia.init_whats()
      time.sleep(30)
    else:
      try:
        list_msg = nova_marcia.list_with_messages_unread()
      except:
        list_msg = []
      have_download = [True if "!download" in x else False for x in list_msg]
      exit_sys = [True if "!exit" in x else False for x in list_msg]
      if True in have_download:
        threads = []
        for contato, msg in nova_marcia.list_with_contact_and_messages_unread():
            if "!download" in msg:
                music_down.params['outtmpl'] = 'musicas/musica_{}.%(ext)s'.format(contato)
                url = msg.split()[1]
                time.sleep(1)
                thread = threading.Thread(target=download_music, args=(contato, url))
                threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

      if True in exit_sys:
          program = False


main()
