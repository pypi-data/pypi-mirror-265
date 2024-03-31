import json
import requests
import threading
import datetime
from tinydb import Query

from mygnuhealth.core import maindb, boldb


class BookofLife():
    """Class that manages the person Book of Life

        Attributes:
        -----------
            boldb: TinyDB instance.
                Holds the book of life with all the events (pages of life)
        Methods:
        --------
            read_book: retrieves all pages
            format_bol: compacts and shows the relevant fields in a
            human readable format
    """

    def format_bol(bookoflife):
        """Takes the necessary fields and formats the book in a way that can
        be shown in the device, mixing fields and compacting entries in a more
        human readable format"""
        book = []
        for pageoflife in bookoflife:
            pol = {}
            dateobj = datetime.datetime.fromisoformat(pageoflife['page_date'])
            # Use a localized and easy to read date format
            date_repr = dateobj.strftime("%a, %b %d '%y\n%H:%M")

            pol['date'] = date_repr
            pol['domain'] = (f"{pageoflife['domain']} "
                             f"({pageoflife['context']})")

            summ = ''
            msr = ''

            title = pageoflife['summary']
            details = pageoflife['info']

            mvals = pageoflife['measurements']

            if title:
                summ = f'{title}\n'

            if ('measurements' in pageoflife.keys() and
                    mvals):
                measure_d = {
                    "bg": ("Blood glucose", "mg/dl"),
                    "hr": ("Heart rate", "bpm"),
                    "wt": ("Weight", "kg"),
                    "bmi": ("BMI", "kg/m2"),
                    "osat": ("osat", "%"),
                }

                for measure in mvals:
                    measure_keys = measure.keys()

                    for key, value in measure_d.items():
                        if key in measure_keys:
                            msr = (f"{msr}{value[0]}: {measure[key]} "
                                   f"{value[1]}\n")

                if 'bp' in mvals[0].keys():

                    msr = (f"{msr}"
                           f"BP: {mvals[0]['bp']['systolic']} / "
                           f"{mvals[0]['bp']['diastolic']} mmHg\n")

                if 'mood_energy' in mvals[0].keys():
                    msr = (f"{msr}"
                           f"mood: {mvals[0]['mood_energy']['mood']}\n"
                           f"energy: {mvals[0]['mood_energy']['energy']}\n")

                summ = summ + msr

                # Include the Lifestyle measures
                if (pageoflife['domain'] == 'lifestyle'):
                    measurements = mvals[0]
                    measurements_keys = measurements.keys()

                    # Show / format the Physical activity values ("pa" key)
                    if 'pa' in measurements_keys:
                        for key, value in measurements['pa'].items():
                            summ = f"{summ}{key}: {value}\n"

                    # Show / format the nutrition values ("nutrition" key)
                    if 'nutrition' in measurements_keys:
                        for key, value in measurements['nutrition'].items():
                            summ = f"{summ}{key}: {value}\n"

                    # Show / format the sleep values ("sleep" key)
                    if 'sleep' in measurements_keys:
                        for key, value in measurements['sleep'].items():
                            summ = f"{summ}{key}: {value}\n"

            if ('genetic_info' in pageoflife.keys() and
                    pageoflife['genetic_info']):
                genetics = pageoflife['genetic_info']
                summ = f'{summ}{genetics}\n'

            if details:
                summ = f'{summ}{details}\n'

            pol['summary'] = summ
            book.append(pol)
        return book

    def read_book():
        """retrieves all pages of the individual Book of Life
        """
        booktable = boldb.table('pol')
        book = booktable.all()
        formatted_bol = BookofLife.format_bol(book)
        return formatted_bol

    def check_sync_status(self):
        fedinfo = maindb.table('federation')
        if len(fedinfo):
            sync = fedinfo.all()[0]['enable_sync']
            return sync

    def sync_book(fedkey):
        # Emit the signal to display a busy indicator while
        # pushing the pages of life to the GH federation
        print("***** Initiating the synchronization \
                with the GH federation server")
        # self.pushingPols.emit()
        # Spawn a new thread so synchronization / pushing is done
        # asynchronously in a non-blocking fashion
        thread = threading.Thread(name="pushpols_thread",
                                  target=BookofLife.push_pols, args=(fedkey,))
        thread.start()

    def push_pols(fedkey):
        """This method will go through each page in the book of life
        that has not been sent to the GNU Health Federation server yet
        (fsynced = False).
        It also checks for records that have a book associated to it
        and that the specific page is has not the "private" flag set.

        Parameters
        ----------
        """
        fedinfo = maindb.table('federation')
        if not len(fedinfo):
            return

        res = fedinfo.all()[0]

        print(res)
        
        # Refresh all pages of life
        booktable = boldb.table('pol')
        book = booktable.all()
        user = res['federation_account']
        protocol = res['protocol']
        server = res['federation_server']
        port = res['federation_port']

        for pol in book:
            timestamp = pol['page_date']
            node = pol['node']
            page_id = pol['page']
            synced = pol['fsynced']

            # Only sync those pages that are not private
            if 'privacy' in pol.keys():
                privacy = pol['privacy']
                if not privacy and not synced:
                    creation_info = {'user': user, 'timestamp': timestamp,
                                     'node': node}

                    pol['creation_info'] = creation_info
                    pol['id'] = page_id

                    url = f"{protocol}://{server}:{port}/pols/{user}/{page_id}"

                    pol['fsynced'] = True
                    send_data = requests.request('POST', url,
                                                 data=json.dumps(pol),
                                                 auth=(user, fedkey),
                                                 verify=False)
                    if send_data:
                        print("Page successfully sent to the GH Federation",
                              send_data.status_code)
                        # Update page of life sync status locally to true
                        print("Setting fsynced to True on page... ", page_id)
                        Page = Query()
                        booktable.update({'fsynced': True},
                                         Page.page == page_id)

                    else:
                        print("Error sending the page.",
                              send_data.status_code)

                else:
                    if privacy:
                        print("This page is private, not syncing", pol)
                    if synced:
                        print("Page already synced", pol)


"""
        # Emit the signal to remove the busy indicator
        print("***** Done pushing PoLs... disabling busy indicator")
        self.finishSyncPols.emit()

    # Signal to emit when the pages of life are being sent to the Federation
    pushingPols = Signal()

    # Signal to emit when the pages of life have been sent
    finishSyncPols = Signal()

    # Property block
    book = Property("QVariantList", read_book, constant=True)

    # Expose to QML the value of sync status
    # It will disable the password field if sync is not enabled.
    sync_status = Property(bool, check_sync_status, constant=True)
"""
