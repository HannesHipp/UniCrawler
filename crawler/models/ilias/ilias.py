from crawler.extraction.dynamic_attribute import DynamicAttribute
from crawler.extraction.locator import ContainsFilter, ExactFilter, Locator, get_attr
from crawler.extraction.html_node import HtmlNode
from crawler.session import Session
from json import loads



class Root(HtmlNode):

    child_types = ['CourseDate'] 
    scope = Locator(
        ExactFilter(
            {'id': 'mainspacekeeper'}
        )
    )
    url_format = {
        'ilias.php?': 'https://ilias3.uni-stuttgart.de/',
        'Uni_Stuttgart/mobs/': 'https://ilias3.uni-stuttgart.de/'
    }
    tree_importance = 0


class CourseDate(Root):

    child_types = ['Course']
    locator = Locator(
        ExactFilter(
            {'class':'panel il-panel-listing-std-container clearfix'}
        ),
        subitem_locator = Locator(
            ExactFilter(
                {'class':'il-item-group'}
            )
        )
    )

    name = DynamicAttribute(
        'text', 
        locator=Locator(
            ExactFilter(
                {'name':'h3'}
            )
        )
    )


class Course(Root):

    child_types = [
        'IlContainerBlock',
        'Folder',
        'OPDFolder',
        'InteractiveVideoFolder',
        'Lm',
        'File',
        'Video',
        'CopaFolder'
    ]
    is_leaf = True
    locator = Locator(
        ContainsFilter(
            {'href':'_crs_'}
        )
    )

    name = DynamicAttribute('string')
    url = DynamicAttribute('href')

    def get_type_hash(self):
        return self.url.split("crs_")[1].split(".html")[0]


class IlContainerBlock(Root):

    child_types = [
        'Folder',
        'OPDFolder',
        'Lm',
        'InteractiveVideoFolder'
    ]
    locator = Locator(
        ExactFilter(
            {'class':'ilContainerBlock container-fluid form-inline'}
        )
    )

    name = DynamicAttribute(
        'text',
        locator=Locator(
            ExactFilter(
                {'name':'h2'}
            )
        )
    )


class Folder(Root):

    child_types = [
        'Folder',
        'Lm',
        'OPDFolder',
        'InteractiveVideoFolder',
        'File',
        'Video'
    ]
    is_leaf = True
    locator = Locator(
        ContainsFilter(
            {'href':'_fold_'}
        )
    )

    name = DynamicAttribute('text')
    url = DynamicAttribute('href')


class File(Root):

    child_types = []
    is_leaf = True
    locator = Locator(
        ContainsFilter(
            {'href':'_file_'}
        )
    )

    name = DynamicAttribute('text')
    url = DynamicAttribute('href')

    def get_type_hash(self):
        return self.url.split("_file_")[1][:7]


class Video(Root):
    
    child_types = []
    is_leaf = True
    locator = Locator(
        ExactFilter(
            {'name':'source'}
        )
    )

    url_format = {
            'ilias.php?': 'https://ilias3.uni-stuttgart.de/',
            'Uni_Stuttgart/mobs/': 'https://ilias3.uni-stuttgart.de/',
            'mh_default_org/api' : 'https://occdn1.tik.uni-stuttgart.de/'
    }
    
    @classmethod
    def get_dynamic_attrs(cls, tag):
        url = get_attr(tag, 'src')	
        return {
            'url': url,
            'name': url.split('?il_wac_token')[0].split('/')[-1]
        }


class Lm(Root):
    
    child_types = [
        'LmNode',
        'LmLeaf'
    ]
    is_leaf = True
    locator = Locator(
        ContainsFilter(
            {'href':'_lm_'}
        )
    )

    name = DynamicAttribute('text')
    url = DynamicAttribute('href')


class LmNode(Root):

    child_types = [
        'LmNode',
        'LmLeaf'
    ]

    name = DynamicAttribute(
        'text',
        locator=Locator(
            ExactFilter(
                {'name':'a'}
            )
        )
    )

    @classmethod
    def find_canidates(cls, parent:HtmlNode):
        if type(parent) is Lm:
            soup = parent.soup.find(id='exp_node_lm_exp_1')
            if not soup:
                return []
            parent.soup = soup
        ul_tag = parent.soup.find('ul')
        if not ul_tag:
            return []
        li_tags = ul_tag.find_all('li', recursive=False)
        return [li_tag for li_tag in li_tags if li_tag.find('ul', recursive=False)]
    

class LmLeaf(Root):

    child_types = [
        'File',
        'Video'
    ]
    is_leaf = True

    name = DynamicAttribute(
        'text',
        locator=Locator(
            ExactFilter(
                {'name':'a'}
            )
        )
    )
    url = DynamicAttribute(
        'href',
        locator=Locator(
            ExactFilter(
                {'name':'a'}
            )
        )
    )

    @classmethod
    def find_canidates(cls, parent:HtmlNode):
        ul_tag = parent.soup.find('ul')
        if not ul_tag:
            return []
        li_tags = ul_tag.find_all('li', recursive=False)
        return [li_tag for li_tag in li_tags if not li_tag.find('ul', recursive=False)]
    
class MCH(Root):

    child_types = ['File', 'Video']
    is_leaf = True
    locator = Locator(
        ContainsFilter(
            {'href':'MediaCastHandler'}
        )
    )

    name = DynamicAttribute('text')
    url = DynamicAttribute('href')

class OPDFolder(Root):

    child_types = ['OPD']
    is_leaf = True
    locator = Locator(
        ContainsFilter(
            {'href':'Cmd=showSeries'}
        )
    )

    name = DynamicAttribute('text')
    url = DynamicAttribute('href')

class OPD(Root):

    child_types = []
    is_leaf = True
    locator = Locator(
        ContainsFilter(
            {'href':'showEpisode'}
        )
    )
    
    def get_dynamic_attrs(tag):
        name = get_attr(tag, 'text')
        if not name:
            raise AttributeError()
        href = get_attr(tag, 'href')
        id = href.split("&id=")[1].split("/")[0]
        id2 = href.split("&id=")[1].split("/")[1]
        json_url = f'https://ilias3.uni-stuttgart.de/Customizing/global/plugins/Services/Repository/RepositoryObject/Opencast/api.php/episode.json?id={id}%2F{id2}'
        json = Session.get_file_content(json_url)
        videos = loads(json)["search-results"]["result"]["mediapackage"]["media"]["track"]
        if len(videos) == 0:
            raise AttributeError()
        if len(videos) > 1:
            videos = [video for video in videos if "presentation" in video["type"]]
        video = videos[0]
        extenstion = video['mimetype'].split('/')[1]
        return {
            'name': f"{name}.{extenstion}",
            'url': video["url"]
        }
    

class InteractiveVideoFolder(Root):

    child_types = ['Video']
    is_leaf = True
    locator = Locator(
        ContainsFilter(
            {'href':'Cmd=showContent'}
        )
    )

    name = DynamicAttribute('text')
    url = DynamicAttribute('href')

# class CopaFolder(Root):

#     child_types = [
#         'CopaSubFolder',
#         'File', 
#         'Video'
#     ]

#     is_leaf = True
#     locator = Locator(
#         ContainsFilter(
#             {'href':'target=copa_'}
#         )
#     )
#     name = DynamicAttribute(
#         'text',
#         locator=Locator(
#             ExactFilter(
#                 {'class':'ilc_text_inline_Strong'}
#             )
#         )
#     )
#     url = DynamicAttribute('href')

#     url_format = {
#         'goto.php': 'https://ilias3.uni-stuttgart.de/'    }

# class CopaSubFolder(Root):

#     child_types = [
#         'CopaSubFolder',
#         'File', 
#         'Video'
#     ]

#     is_leaf = True
#     locator = Locator(
#         ContainsFilter(
#             {'href':'target=copa_'}
#         )
#     )
#     name = DynamicAttribute(
#         'text',
#         locator=Locator(
#             ExactFilter(
#                 {'class':'ilc_Paragraph ilc_text_block_Kapitelueberschrift ilc_link_ExtLink'}
#             )
#         )
#     )
#     url = DynamicAttribute('href')

#     url_format = {
#         'goto.php': 'https://ilias3.uni-stuttgart.de/'   
#     }