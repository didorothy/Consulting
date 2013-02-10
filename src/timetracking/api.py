import datetime

from jsonrpc import jsonrpc_method

import models


@jsonrpc_method('timetracking.get_time_entries() -> list', authenticated=True, validate=True)
def get_time_entries(request):
    '''Returns all time entries.'''
    #TODO: limit this somehow.
    entries = []
    for e in models.TimeEntry.objects.all():
        entries.append(e.__dict__)
    
    return entries

@jsonrpc_method('timetracking.get_projects() -> list', authenticated=True, validate=True)
def get_projects(request):
    '''Returns a list of all projects.'''
    projects = []
    for p in models.Project.objects.all():
        projects.append(p.__dict__)
    
    return projects

@jsonrpc_method('timetracking.add_time_entry(project=int, start=str, stop=str, description=str) -> int', authenticated=True, validate=True)
def add_time_entry(request, project, start, stop, description):
    '''Creates a TimeEntry for a specific project.'''
    
    project = models.Project.objects.get(id=int(project))
    start = datetime.datetime.strptime(start, 'Y-m-d H:M:s')
    stop = datetime.datetime.strptime(stop, 'Y-m-d H:M:s')
    
    entry = models.TimeEntry()
    entry.project = project
    entry.start = start
    entry.stop = stop
    entry.description = description
    
    try:
        entry.save()
        
        return entry.id
    except:
        # something went wrong when saving so send back a failure message.
        return -1

