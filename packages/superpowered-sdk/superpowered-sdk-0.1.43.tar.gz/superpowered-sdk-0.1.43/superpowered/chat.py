import time

from . import superpowered
from . import exceptions


def create_chat_thread(knowledge_base_ids: list[str] = None, supp_id: str = None, model: str = None, temperature: float = None, segment_length: str = None, system_message: str = None, title: str = None, use_rse: bool = None, response_length: str = None, auto_query_guidance: str = None, use_web_search: bool = None, web_search_include_domains: list = None, web_search_exclude_domains: list = None, web_search_start_date: str = None, web_search_end_date: str = None, web_search_timeframe_days: int = None, web_search_preset_id: str = None, json_response: bool = None) -> dict:
    """
    Create a chat thread. Chat threads are used to store the state of a conversation.

    Args:
        knowledge_base_ids (list[str], optional): A list of knowledge base IDs to use for the thread. Defaults to None.
        supp_id (str, optional): A supp ID to use for the thread. This will also be used for the ``supp_id`` field in the associated chat request billable events. Defaults to None.
        model (str, optional): The model to use for the thread. Defaults to None.
        temperature (float, optional): The temperature to use for the thread. Defaults to None.
        system_message (str, optional): The system message to use for the thread. Defaults to None.
        auto_query_guidance (str, optional): When we automatically generate queries based on user input, you may want to provide some additional guidance and/or context to the system. Defaults to ''.
        title (str, optional): The title to use for the thread. Defaults to None.
        use_rse (bool, optional): Whether or not to use Relevant Segment Extraction (RSE). Defaults to True.
        segment_length (str, optional): Ignored if `use_rse` is False. This parameter determines how long each result (segment) is. Defaults to 'medium'. Must be one of 'very_short', 'short', 'medium', or 'long'.
        response_length (str, optional): This parameter determines how long the response is. Defaults to 'medium'. Must be one of 'short', 'medium', or 'long'.
        use_web_search (bool, optional): Whether or not to use web search. Defaults to False.
        web_search_include_domains (list, optional): A list of domains to include in the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_exclude_domains (list, optional): A list of domains to exclude in the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_start_date (str, optional): The start date to use for the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_end_date (str, optional): The end date to use for the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_timeframe_days (int, optional): The number of days to use for the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_preset_id (str, optional): The ID of the web search preset to use. Ignored if ``use_web_search`` is False. Takes precedence over other web search parameters. Defaults to None.
        json_response (bool, optional): Whether to return the response in JSON format. If false, the response will be in plain text format. ``NOTE:`` This parameter can only be set when the model is an OpenAI model or a Mistral model (currently only `mistral-small` and `mistral-large` with the others to follow soon). Defaults to False.

    Note:
        All parameters besides ``supp_id`` are the thread's default options. These options can be overridden when using the ``get_chat_response()`` function.

    Returns:
        dict: A chat thread object.

    References:
        ``POST /chat/threads``
    """
    data = {
        'default_options': {}
    }
    web_search_config = {}
    if supp_id:
        data['supp_id'] = supp_id
    if title:
        data['title'] = title
    if knowledge_base_ids:
        data['default_options']['knowledge_base_ids'] = knowledge_base_ids
    if model:
        data['default_options']['model'] = model
    if temperature:
        data['default_options']['temperature'] = temperature
    if segment_length:
        data['default_options']['segment_length'] = segment_length
    if response_length:
        data['default_options']['response_length'] = response_length
    if system_message:
        data['default_options']['system_message'] = system_message
    if auto_query_guidance:
        data['default_options']['auto_query_guidance'] = auto_query_guidance
    if use_rse is not None:
        data['default_options']['use_rse'] = use_rse
    if json_response is not None:
        data['default_options']['json_response'] = json_response
    if use_web_search:
        data['default_options']['use_web_search'] = use_web_search
    if web_search_include_domains:
        web_search_config['include_domains'] = web_search_include_domains
    if web_search_exclude_domains:
        web_search_config['exclude_domains'] = web_search_exclude_domains
    if web_search_start_date:
        web_search_config['start_date'] = web_search_start_date
    if web_search_end_date:
        web_search_config['end_date'] = web_search_end_date
    if web_search_timeframe_days:
        web_search_config['timeframe_days'] = web_search_timeframe_days
    if web_search_preset_id:
        web_search_config['web_search_preset_id'] = web_search_preset_id

    if web_search_config:
        data['default_options']['web_search_config'] = web_search_config

    args = {
        'method': 'POST',
        'url': f'{superpowered.get_base_url()}/chat/threads',
        'json': data,
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)


def list_chat_threads(supp_id: str = None) -> dict:
    """
    List chat threads.

    Args:
        supp_id (str, optional): The supp_id of the thread. Defaults to None.

    Returns:
        dict: A list of chat thread objects.
    
    References:
        ``GET /chat/threads``
    """
    params = {}
    if supp_id:
        params['supp_id'] = supp_id

    args = {
        'method': 'GET',
        'url': f'{superpowered.get_base_url()}/chat/threads',
        'auth': superpowered.auth(),
        'params': params,
    }
    resp = superpowered.make_api_call(args)
    threads = resp.get('chat_threads', [])

    while resp.get('next_page_token'):
        args['params']['next_page_token'] = resp['next_page_token']
        resp = superpowered.make_api_call(args)
        threads.extend(resp.get('chat_threads', []))

    return threads


def get_chat_thread(thread_id: str) -> dict:
    """
    Get a chat thread.

    Args:
        thread_id (str): The ID of the thread.

    Returns:
        dict: A chat thread object.

    References:
        ``GET /chat/threads/{thread_id}``
    """
    args = {
        'method': 'GET',
        'url': f'{superpowered.get_base_url()}/chat/threads/{thread_id}',
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)


def update_chat_thread(thread_id: str, knowledge_base_ids: list[str] = None, supp_id: str = None, model: str = None, temperature: float = None, segment_length: str = None, system_message: str = None, title: str = None, use_rse: bool = None, response_length: str = None, auto_query_guidance: str = None, use_web_search: bool = None, web_search_include_domains: list = None, web_search_exclude_domains: list = None, web_search_start_date: str = None, web_search_end_date: str = None, web_search_timeframe_days: int = None, web_search_preset_id: str = None, json_response: bool = None) -> dict:
    """
    Update a chat thread.

    Args:
        thread_id (str): The ID of the thread.
        knowledge_base_ids (list[str], optional): A list of knowledge base IDs to use for the thread. Defaults to None.
        supp_id (str, optional): A supp ID to use for the thread. This will also be used for the ``supp_id`` field in the associated chat request billable events. Defaults to None.
        model (str, optional): The model to use for the thread. Defaults to None.
        temperature (float, optional): The temperature to use for the thread. Defaults to None.
        system_message (str, optional): The system message to use for the thread. Defaults to None.
        auto_query_guidance (str, optional): When we automatically generate queries based on user input, you may want to provide some additional guidance and/or context to the system. Defaults to None.
        title (str, optional): The title to use for the thread. Defaults to None.
        use_rse (bool, optional): Whether or not to use Relevant Segment Extraction (RSE). Defaults to None.
        segment_length (str, optional): Ignored if `use_rse` is False. This parameter determines how long each result (segment) is. Defaults to None. Must be one of 'very_short', 'short', 'medium', or 'long'.
        response_length (str, optional): This parameter determines how long the response is. Must be one of 'short', 'medium', or 'long'.
        use_web_search (bool, optional): Whether or not to use web search. Defaults to None.
        web_search_include_domains (list, optional): A list of domains to include in the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_exclude_domains (list, optional): A list of domains to exclude in the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_start_date (str, optional): The start date to use for the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_end_date (str, optional): The end date to use for the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_timeframe_days (int, optional): The number of days to use for the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_preset_id (str, optional): The ID of the web search preset to use. Ignored if ``use_web_search`` is False. Takes precedence over other web search parameters. Defaults to None.
        json_response (bool, optional): Whether to return the response in JSON format. If false, the response will be in plain text format. ``NOTE:`` This parameter can only be set when the model is an OpenAI model or a Mistral model (currently only `mistral-small` and `mistral-large` with the others to follow soon). Defaults to None.

    Returns:
        dict: A chat thread object.

    References:
        ``PATCH /chat/threads/{thread_id}``
    """
    data = {
        'default_options': {}
    }
    default_options = {}
    web_search_config = {}
    if supp_id:
        data['supp_id'] = supp_id
    if title:
        data['title'] = title
    if knowledge_base_ids:
        default_options['knowledge_base_ids'] = knowledge_base_ids
    if model:
        default_options['model'] = model
    if temperature:
        default_options['temperature'] = temperature
    if segment_length:
        default_options['segment_length'] = segment_length
    if response_length:
        default_options['response_length'] = response_length
    if system_message:
        default_options['system_message'] = system_message
    if auto_query_guidance:
        default_options['auto_query_guidance'] = auto_query_guidance
    if use_rse is not None:
        default_options['use_rse'] = use_rse
    if json_response is not None:
        default_options['json_response'] = json_response
    if use_web_search:
        default_options['use_web_search'] = use_web_search
    if web_search_include_domains:
        web_search_config['include_domains'] = web_search_include_domains
    if web_search_exclude_domains:
        web_search_config['exclude_domains'] = web_search_exclude_domains
    if web_search_start_date:
        web_search_config['start_date'] = web_search_start_date
    if web_search_end_date:
        web_search_config['end_date'] = web_search_end_date
    if web_search_timeframe_days:
        web_search_config['timeframe_days'] = web_search_timeframe_days
    if web_search_preset_id:
        web_search_config['web_search_preset_id'] = web_search_preset_id

    if web_search_config:
        default_options['web_search_config'] = web_search_config

    if default_options:
        data['default_options'] = default_options

    args = {
        'method': 'PATCH',
        'url': f'{superpowered.get_base_url()}/chat/threads/{thread_id}',
        'json': data,
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)


def delete_chat_thread(thread_id: str) -> dict:
    """
    Delete a chat thread.

    Args:
        thread_id (str): The ID of the thread.

    Returns:
        dict: A chat thread object.

    References:
        ``DELETE /chat/threads/{thread_id}``
    """
    args = {
        'method': 'DELETE',
        'url': f'{superpowered.get_base_url()}/chat/threads/{thread_id}',
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)


def get_chat_response(thread_id: str, input: str, knowledge_base_ids: list = None, model: str = None, temperature: float = None, system_message: str = None, use_rse: bool = None, segment_length: str = None, response_length: str = None, timeout: int = 90, auto_query_guidance: str = None, use_web_search: bool = None, web_search_include_domains: list = None, web_search_exclude_domains: list = None, web_search_start_date: str = None, web_search_end_date: str = None, web_search_timeframe_days: int = None, web_search_preset_id: str = None, json_response: bool = None) -> dict:
    """
    Get a response for a specific chat thread. This endpoint uses a tool we call "Auto Query" to reformulate queries to the knowledge base given the recent chat history as well as user input.

    Note:
        To ensure "Auto Query" works as well as it can, please ensure the knowledge bases you are using have good titles and descriptions. If you are only querying from a single knowledge base, this doesn't matter.

    Args:
        thread_id (str): The ID of the thread.
        input (str): The user's input.
        knowledge_base_ids (list, optional): A list of knowledge base IDs to use for the thread. **These override any default config options defined in the thread itself**. Defaults to None.
        model (str, optional): The model to use for the thread. **This overrides any default config options defined in the thread itself**. Defaults to None.
        temperature (float, optional): The temperature to use for the thread. **This overrides any default config options defined in the thread itself**. Defaults to None.
        system_message (str, optional): The system message to use for the thread. **This overrides any default config options defined in the thread itself**. Defaults to None.
        auto_query_guidance (str, optional): When we automatically generate queries based on user input, you may want to provide some additional guidance and/or context to the system. **This overrides any default config options defined in the thread itself**. Defaults to None.
        use_rse (bool, optional): Whether or not to use Relevant Segment Extraction (RSE). **This overrides any default config options defined in the thread itself**. Defaults to None.
        segment_length (str, optional): Ignored if `use_rse` is False. This parameter determines how long each result (segment) is. Must be one of 'very_short', 'short', 'medium', or 'long'. **This overrides any default config options defined in the thread itself**. Defaults to None.
        response_length (str, optional): This parameter determines how long the response is. Must be one of 'short', 'medium', or 'long'. **This overrides any default config options defined in the thread itself**. Defaults to None.
        use_web_search (bool, optional): Whether or not to use web search. Defaults to None.
        web_search_include_domains (list, optional): A list of domains to include in the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_exclude_domains (list, optional): A list of domains to exclude in the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_start_date (str, optional): The start date to use for the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_end_date (str, optional): The end date to use for the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_timeframe_days (int, optional): The number of days to use for the web search. Ignored if ``use_web_search`` is False. Defaults to None.
        web_search_preset_id (str, optional): The ID of the web search preset to use. Ignored if ``use_web_search`` is False. Takes precedence over other web search parameters. Defaults to None.
        json_response (bool, optional): Whether to return the response in JSON format. If false, the response will be in plain text format. ``NOTE:`` This parameter can only be set when the model is an OpenAI model or a Mistral model (currently only `mistral-small` and `mistral-large` with the others to follow soon). Defaults to None.
        
    Returns:
        dict: A chat response object.

    References:
        ``POST /chat/threads/{thread_id}/get_response``
    """
    data = {
        'async': True,
        'input': input,
    }
    web_search_config = {}
    if knowledge_base_ids:
        data['knowledge_base_ids'] = knowledge_base_ids
    if model:
        data['model'] = model
    if temperature:
        data['temperature'] = temperature
    if system_message:
        data['system_message'] = system_message
    if auto_query_guidance:
        data['auto_query_guidance'] = auto_query_guidance
    if use_rse is not None:
        data['use_rse'] = use_rse
    if segment_length:
        data['segment_length'] = segment_length
    if response_length:
        data['response_length'] = response_length
    if json_response is not None:
        data['json_response'] = json_response
    if use_web_search:
        data['use_web_search'] = use_web_search
    if web_search_include_domains:
        web_search_config['include_domains'] = web_search_include_domains
    if web_search_exclude_domains:
        web_search_config['exclude_domains'] = web_search_exclude_domains
    if web_search_start_date:
        web_search_config['start_date'] = web_search_start_date
    if web_search_end_date:
        web_search_config['end_date'] = web_search_end_date
    if web_search_timeframe_days:
        web_search_config['timeframe_days'] = web_search_timeframe_days
    if web_search_preset_id:
        web_search_config['web_search_preset_id'] = web_search_preset_id

    if web_search_config:
        data['web_search_config'] = web_search_config

    args = {
        'method': 'POST',
        'url': f'{superpowered.get_base_url()}/chat/threads/{thread_id}/get_response',
        'json': data,
        'auth': superpowered.auth(),
    }
    resp = superpowered.make_api_call(args)
    t0 = time.time()
    while time.time() - t0 < timeout and resp.get('status') in {'PENDING', 'IN_PROGRESS'}:
        time.sleep(1)
        args = {
            'method': 'GET',
            'url': resp['status_url'],
            'auth': superpowered.auth(),
        }
        resp = superpowered.make_api_call(args)
    if resp['status'] == 'FAILED':
        raise exceptions.InternalServerError
    else:
        return resp['response']


def list_thread_interactions(thread_id: str, order: str = None) -> dict:
    """
    List interactions for a chat thread.

    Args:
        thread_id (str): The ID of the thread.
        order (str, optional): The order to return the interactions in. Must be `asc` or `desc`. Defaults to `desc`.

    Returns:
        dict: A list of chat interaction objects.

    References:
        ``GET /chat/threads/{thread_id}/interactions``
    """
    params = {}
    if order:
        if order.lower() not in ['asc', 'desc']:
            raise ValueError('`order` parameter must be "asc" or "desc"')
        params['order'] = order.lower()

    args = {
        'method': 'GET',
        'url': f'{superpowered.get_base_url()}/chat/threads/{thread_id}/interactions',
        'auth': superpowered.auth(),
        'params': params,
    }
    resp = superpowered.make_api_call(args)
    interactions = resp.get('interactions', [])

    while resp.get('next_page_token'):
        args['params']['next_page_token'] = resp['next_page_token']
        resp = superpowered.make_api_call(args)
        interactions.extend(resp.get('interactions', []))

    return interactions
